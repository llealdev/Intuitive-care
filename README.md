
# ANS Data Pipeline

Este projeto tem como objetivo coletar, transformar, armazenar e disponibilizar dados sobre operadoras de planos de saúde registradas na **Agência Nacional de Saúde Suplementar (ANS)**. A solução inclui automação de download de arquivos, extração e limpeza de dados, estruturação em banco de dados e disponibilização via API.

## 📂 Estrutura do Projeto

O projeto está dividido em quatro principais módulos:

```
intuitive-care/
│-- web_scraping/          # Coleta de dados da ANS
│-- data_transformation/   # Extração e limpeza dos dados
│-- database/              # Estruturação e análise dos dados
│-- api/                   # API para acesso aos dados e frontend
│-- intuitive-care-postman-collection.json        # Arquivos da collection do Postman
│-- docker-compose.yml     # Configuração do ambiente Docker
│-- README.md              # Documentação principal
```

---

## 1️⃣ Web Scraping - ANSScraper

Este módulo baixa automaticamente os arquivos PDF da ANS contendo a atualização do rol de procedimentos.

### 🚀 Tecnologias Utilizadas
- **Python**
- **Requests** - Requisições HTTP
- **BeautifulSoup** - Extração de links
- **ThreadPoolExecutor** - Download paralelo
- **Zipfile** - Compactação dos arquivos
- **Logging** - Monitoramento

### 🛠 Como Executar

1. Instale as dependências:
   ```sh
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```
2. Execute o script:
   ```sh
   python web_scraping/ans_scraper.py
   ```
   - Os PDFs serão baixados para `output/`
   - O arquivo `anexos.zip` será gerado

---

## 2️⃣ Transformação de Dados

O módulo **extrai e limpa** dados tabulares dos PDFs usando `tabula-py` e `pandas`.

### 🚀 Tecnologias Utilizadas
- **Python**
- **tabula-py** - Extração de tabelas de PDFs
- **pandas** - Limpeza e manipulação de dados

### 🛠 Como Executar

1. Instale as dependências:
   ```sh
   pip install pandas tabula-py
   ```
   **Obs:** Certifique-se de ter o Java instalado para o `tabula-py`.

2. Coloque os arquivos PDF na pasta `input/`.

3. Execute o script:
   ```sh
   python data_transformation/extract_table.py
   ```
   - O CSV limpo será salvo em `output/Rol_Procedimentos.csv`
   - Um ZIP contendo os dados será gerado em `output/`
   - O processo será registrado em `transform.log`

---

## 3️⃣ Banco de Dados

Os dados extraídos são estruturados em um banco PostgreSQL, permitindo análises sobre as operadoras de saúde.

### 🚀 Tecnologias Utilizadas
- **PostgreSQL**
- **Docker**
- **SQL para consultas analíticas**

### 🛠 Como Configurar

1. Suba o ambiente Docker:
   ```sh
   docker-compose up -d
   ```
2. Acesse o PgAdmin:
   - URL: [http://localhost:5050](http://localhost:5050)
   - Usuário: `admin@ans.com`
   - Senha: `admin123`
3. Execute os scripts SQL:
   ```sh
   docker exec -it ans_postgres bash
   psql -U ans_admin -d ans_db
   \i /scripts/01_setup.sql;
   \i /scripts/02_import.sql;
   \i /scripts/03_analytics.sql;
   ```

### 📊 Consultas Analíticas

- **Top 10 Operadoras com Maiores Despesas no Último Trimestre**
- **Top 10 Operadoras com Maiores Despesas no Último Ano**

Os scripts SQL correspondentes podem ser encontrados em `database/scripts/`.

---

## 4️⃣ API e Frontend

A API permite acesso aos dados e o frontend fornece uma interface para consultas.

### 🚀 Tecnologias Utilizadas
- **FastAPI** - Backend
- **Node.js** - Frontend (React)
- **Docker**

### 🛠 Como Executar

#### 🔹 Backend

1. Instale as dependências:
   ```sh
   pip install -r api/backend/requirements.txt
   ```
2. Execute o servidor FastAPI:
   ```sh
   uvicorn api.backend.src.main:app --reload --port 8080
   ```
3. Acesse a documentação da API:  
   [http://localhost:8080/docs](http://localhost:8080/docs)

#### 🔹 Frontend

1. Instale as dependências:
   ```sh
   cd api/frontend
   npm install
   ```
2. Inicie o frontend:
   ```sh
   npm start
   ```

---

## 📬 Testando a API no Postman

Para facilitar a consulta dos dados, foi criada uma **Collection no Postman** chamada **"intuitive-care"**.  

### 🔗 Link para a Collection  
Você pode acessar e importar a Collection diretamente pelo link abaixo:  
[Importar Collection no Postman](https://matheusleal-58517.postman.co/workspace/Matheus-Leal's-Workspace~080349ba-08ac-4554-86b9-96bbda2fcfad/collection/43611296-c8959fdb-c807-4344-a158-9ee2de106bca?action=share&source=collection_link&creator=43611296)

### 📌 Endpoints Disponíveis

- **Buscar operadoras de saúde por nome (com limite de resultados)**  
  **GET** `http://localhost:8080/api/operadoras?q=Itau&limit=10`

  **Exemplo de resposta:**
  ```json
  [
    {
      "id": 1,
      "nome": "Itau Seguros de Saúde",
      "registro": "123456",
      "cnpj": "12.345.678/0001-90",
      "tipo": "Administradora de Benefícios",
      "status": "Ativa"
    },
    ...
  ]
  ```

- **Consultar detalhes de uma operadora específica**  
  **GET** `http://localhost:8080/api/operadoras/{id}`

- **Obter estatísticas sobre operadoras**  
  **GET** `http://localhost:8080/api/estatisticas`

### 📥 Importação Manual  

Caso prefira importar manualmente a Collection, você pode baixar o arquivo `intuitive-cafe-postman-collection.json` localizado no diretório `/postman/` e importá-lo no Postman.

---

## ✅ Conclusão

Este projeto integra **Web Scraping, Transformação de Dados, Banco de Dados e API** para fornecer informações estruturadas sobre operadoras de saúde da ANS. Ele permite:

✔️ **Coleta automática** de documentos oficiais  
✔️ **Extração e limpeza** de dados tabulares  
✔️ **Armazenamento** em um banco relacional otimizado  
✔️ **Acesso via API** para análise e consulta  
✔️ **Testes e visualização de dados via Postman**  

Caso tenha dúvidas ou precise modificar alguma funcionalidade, consulte a documentação de cada módulo ou me chame pelo linkedin.
