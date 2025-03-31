# Extração e Limpeza de Dados de PDFs

Este projeto tem como objetivo extrair e limpar dados de documentos PDF contendo tabelas de procedimentos. A extração é realizada utilizando a biblioteca `tabula`, e a limpeza de dados é feita com `pandas`.

## Estrutura do Projeto

```
project_root/
│-- data_transformation/
│   │-- data_cleaner.py  # Funções para limpeza de dados
│   │-- extract_table.py  # Extração de tabelas do PDF
│-- input/  # Diretório onde os arquivos PDF devem ser colocados
│-- output/ # Diretório onde serão salvos os arquivos processados
│-- transform.log  # Log do processamento
```

## Dependências

Para rodar este projeto, instale as seguintes dependências:

```bash
pip install pandas tabula-py
```

**OBS:** Certifique-se de ter o Java instalado, pois o `tabula-py` depende dele.

## Como Executar

1. Coloque o arquivo PDF (por exemplo, `Anexo_I.pdf`) na pasta `input/`.
2. Execute o script de extração:

```bash
python data_transformation/extract_table.py
```

3. Se o processo for bem-sucedido:
   - O CSV com os dados extraídos e limpos será salvo em `output/Rol_Procedimentos.csv`.
   - Um arquivo ZIP contendo o CSV será criado em `output/`.
   - O log do processamento pode ser encontrado no arquivo `transform.log`.

## Funcionalidades

- ``: Responsável pela limpeza dos dados, padronizando cabeçalhos e substituindo abreviações.
- ``: Realiza a extração de tabelas de PDFs, remove cabeçalhos duplicados e salva os dados processados.

## Logs

O arquivo `transform.log` registrará todas as etapas do processamento, incluindo erros que possam ocorrer durante a extração ou a limpeza de dados.
