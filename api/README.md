# API e Frontend - Operadoras de Saúde

Este projeto consiste em uma API desenvolvida com FastAPI e um frontend utilizando Node.js. O objetivo é fornecer uma interface para busca de operadoras de saúde com base em um arquivo CSV.

## Estrutura do Projeto

```
intuitive-care/
│-- api/
│   │-- backend/  # Código do backend (FastAPI)
│   │-- frontend/ # Código do frontend (React ou outra tecnologia)

```

## Dependências

Antes de rodar o projeto, instale as dependências necessárias.

### Backend

Instale as dependências do backend executando:

```bash
pip install -r requirements.txt
```

**Lista de dependências:**

```txt
annotated-types==0.7.0
anyio==4.9.0
fastapi==0.115.12
idna==3.10
numpy==2.2.4
pandas==2.2.3
pydantic==2.11.1
pydantic_core==2.33.0
python-dateutil==2.9.0.post0
python-dotenv==1.1.0
pytz==2025.2
six==1.17.0
sniffio==1.3.1
starlette==0.46.1
typing-inspection==0.4.0
typing_extensions==4.13.0
tzdata==2025.2
unicorn==2.1.3
```

### Frontend

Instale as dependências do frontend executando:

```bash
npm install
```

## Como Executar

### Rodando o Backend

1. Navegue até a pasta do backend:
   ```bash
   cd api/backend
   ```
2. Execute o servidor FastAPI com o Uvicorn:
   ```bash
   uvicorn src.main:app --reload --port 8080
   ```
3. Acesse a documentação da API no navegador:
   [http://localhost:8080/docs](http://localhost:8080/docs)

### Rodando o Frontend

1. Navegue até a pasta do frontend:
   ```bash
   cd api/frontend
   ```
2. Instale as dependências:
   ```bash
   npm install
   ```
3. Inicie o servidor de desenvolvimento:
   ```bash
   npm run dev
   ```

## Funcionalidades da API

A API disponibiliza um endpoint para buscar operadoras de saúde.

### Endpoint `/api/operadoras`

- **Método:** `GET`
- **Parâmetros:**
  - `q` (opcional) → Termo de busca
  - `limit` (opcional) → Número máximo de resultados
- **Resposta:** JSON contendo as operadoras encontradas.

```json
{
  "success": true,
  "count": 10,
  "results": [
    {
      "Razao_Social": "Nome da Operadora",
      "Nome_Fantasia": "Fantasia",
      "CNPJ": "00.000.000/0001-00"
    }
  ]
}
```

## Logs

O backend registra logs de execução e possíveis erros durante o processamento.

---



