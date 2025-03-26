# ANSScraper - Documentação

## Visão Geral

Este projeto tem como objetivo automatizar o download de arquivos PDF da página da ANS (Agência Nacional de Saúde Suplementar) que contém a atualização do rol de procedimentos. O script busca os links dos arquivos, faz o download de forma paralela e os compacta em um arquivo ZIP.

## Tecnologias Utilizadas

- **Python**
- **Requests** para realizar requisições HTTP
- **BeautifulSoup** para fazer a extração dos links dos arquivos
- **ThreadPoolExecutor** para download paralelo
- **Zipfile** para compactação dos arquivos
- **Logging** para monitoramento do processo

## Como Executar o Projeto

### 1. Instalação das Dependências

Crie um ambiente virtual e instale as dependências:

```sh
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Executando o Script

Basta rodar o script principal:

```sh
python ans_scraper.py
```

O script irá criar um diretório `output/`, baixar os arquivos PDF e compactá-los em `output/anexos.zip`.

## Explicação do Código

### Importação de Bibliotecas

```python
import logging
from pathlib import Path
import requests 
from bs4 import BeautifulSoup
import zipfile
from concurrent.futures import ThreadPoolExecutor
```

Essas bibliotecas permitem manipular arquivos e diretórios, fazer requisições HTTP, processar HTML, baixar arquivos e compactá-los.

### Classe `ANSScraper`

A classe define o scraper e suas funcionalidades.

#### `__init__` - Inicialização da Sessão

```python
self.base_url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
self.session = requests.Session()
self.session.headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)',
    'Accept-Language': 'pt-BR,pt;q=0.9'
})
```

Cria uma sessão HTTP e define cabeçalhos para evitar bloqueios do servidor.

#### `_download_file` - Baixa um arquivo PDF

```python
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
```

Baixa um arquivo da URL informada e o salva no diretório de saída.

#### `run` - Processo Principal

1. Cria o diretório `output/` se não existir.
2. Faz uma requisição para obter a página HTML.
3. Extrai os links dos arquivos PDF.
4. Baixa os arquivos em paralelo.
5. Compacta os PDFs em um arquivo ZIP.

```python
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)
```

```python
pdfs = [ 
    a['href'] for a in soup.select('a[href$=".pdf"]')
    if 'Anexo_I' in a['href'] or 'Anexo_II' in a['href']
] 
```

Extrai apenas os PDFs que possuem "Anexo_I" ou "Anexo_II" no nome.

```python
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
```

Realiza o download dos arquivos de forma assíncrona.

```python
zip_path = output_dir / "anexos.zip"
with zipfile.ZipFile(zip_path, 'w') as zipf:
    for file in output_dir.glob('*.pdf'):
        zipf.write(file, arcname=file.name)
        logging.info(f"Arquivo {file.name} adicionado ao ZIP")
```

Cria um arquivo ZIP contendo todos os PDFs baixados.

### Configuração de Logging

```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('scraping.log'), logging.StreamHandler()]
)
```

Define logs para depuração e acompanhamento do processo.

## Arquivo `requirements.txt`

```txt
beautifulsoup4==4.13.3
certifi==2025.1.31
charset-normalizer==3.4.1
idna==3.10
requests==2.32.3
soupsieve==2.6
typing_extensions==4.13.0
urllib3==2.3.0
```

Lista de dependências para instalar o projeto.

## Conclusão

Este scraper automatiza o download de arquivos da ANS, facilitando o acesso a documentos importantes. O uso de *web scraping*, *multithreading* e *arquivos ZIP* tornam o processo rápido e eficiente. Caso haja necessidade de ajustes, basta modificar os filtros na extração dos PDFs ou os parâmetros de execução.
