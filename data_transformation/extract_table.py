import tabula
import pandas as pd
from pathlib import Path
import logging 
import zipfile
import re
from data_cleaner import clean_data

# Configurações de logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('transform.log'), logging.StreamHandler()]   
)

class PDFTransformer:
    def __init__(self):
        self.input_dir = Path("input")
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        self.header_regex = re.compile(
            r'PROCEDIMENTO\s+RN\s*\(alteração\)\s*VIGÊNCIA\s+OD\s+AMB\s+HCO\s+HSO\s+REF\s+PAC\s+DUT\s+SUBGRUPO\s+GRUPO\s+CAPÍTULO',
            re.IGNORECASE
        )

    def is_header_row(self, row):
        # Verifica se a linha é um cabeçalho
        combined_text = ' '.join(str(cell) for cell in row if pd.notna(cell))
        return bool(self.header_regex.search(combined_text))

    def extract_tables(self, pdf_path: Path) -> pd.DataFrame:
        # Extrai todas as tabelas do PDF usando o tabula-py
        try:
            logging.info(f"Iniciando extração do arquivo: {pdf_path.name}")

            tables = tabula.read_pdf(
                str(pdf_path),
                pages='all',
                multiple_tables=True,
                lattice=True,
                pandas_options={'header': None},
                silent=True
            )

            cleaned_tables = []
            for table in tables:
                # Remove linhas de cabeçalho
                mask = table.apply(lambda row: not self.is_header_row(row),axis=1)
                filtered_table = table[mask]

                # Remove linhas vazias
                filtered_table = filtered_table.dropna(how='all')

                if not filtered_table.empty:
                    cleaned_tables.append(filtered_table)

            if not cleaned_tables:
                raise ValueError("Nenhuma tabela válida encontrada após filtrar cabeçalhos")
            
            df = pd.concat(cleaned_tables, ignore_index=True)
            logging.info(f"Extraídas {len(df)} linhas do PDF")
            return df

        except Exception as e:
            logging.error(f"Falha na extração: {str(e)}")
            raise
    
    def process_anexo_i(self):
        # Processa o Anexo I conforme requisitos

        try:
            # Encontra o PDF do Anexo I
            pdf_file = next(self.input_dir.glob("Anexo_I*.pdf"))

            # Extrai os dados 
            df = self.extract_tables(pdf_file)

            # Limpeza dos dados 
            df = clean_data(df)

            # Salva como CSV
            csv_path = self.output_dir / "Rol_Procedimentos.csv"
            df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            logging.info(f"CSV salvo em: {csv_path}")

            #Cria arquivo ZIP
            self._create_zip(csv_path)
            
            return True

        except Exception as e:
            logging.critical(f"Falha bo processamento: {str(e)}")
            return False

    def _create_zip(self, csv_path: Path):
        # Cria arquivo ZIP com o CSV

        zip_path = self.output_dir / f"Teste_Matheus_Leal.zip"
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(csv_path, arcname=csv_path.name)
        logging.info(f"Arquivo ZIP criado: {zip_path}")

if __name__ == "__main__":
    transformer = PDFTransformer()
    transformer.process_anexo_i()
