import logging
from pathlib import Path
import requests 
from bs4 import BeautifulSoup
import zipfile
from concurrent.futures import ThreadPoolExecutor

class ANSScraper:
    
    def __init__(self):
        
        self.base_url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)',
            'Accept-Language': 'pt-BR,pt;q=0.9'
        })

    def _download_file(self, url: str, save_path: Path) -> None:
        try:
            with self.session.get(url, stream=True, timeout=60) as r:
                r.raise_for_status()
                with open(save_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            
            logging.info(f"Baixado o arquivo: {save_path.name}")
        except Exception as e:
            logging.error(f"Falha ao baixar o arquivo: {save_path.name}")
            raise

    def run(self):
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        try:
            # Extrair links dos PDFs
            response = self.session.get(self.base_url, timeout=30)
            soup = BeautifulSoup(response.text, 'html.parser')
            pdfs = [ 
                a['href'] for a in soup.select('a[href$=".pdf"]')
                if 'Anexo_I' in a['href'] or 'Anexo_II' in a['href']
            ] 

            # Download em paralelo 
            with ThreadPoolExecutor(max_workers=3) as executor:
                futures = []
                for pdf_url in pdfs:
                    filename = pdf_url.split('/')[-1]
                    futures.append(
                        executor.submit(
                            self._download_file,
                            pdf_url,
                            output_dir / filename
                        )
                    )   

            # Compactando os arquivos
            zip_path = output_dir / "anexos.zip"
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for file in output_dir.glob('*.pdf'):
                    zipf.write(file, arcname=file.name)
                    logging.info(f"Arquivo {file.name} adicionado ao ZIP")

            return True
        except Exception as e:
            logging.critical(f"Falha crítica: {str(e)}")
            return False 

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.FileHandler('scraping.log'), logging.StreamHandler()]
    )
    ANSScraper().run()