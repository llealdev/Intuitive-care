# Projeto de Banco de Dados ANS

## Visão Geral
Este projeto tem como objetivo estruturar um banco de dados para armazenar informações sobre operadoras de planos de saúde registradas na ANS e suas demonstrações contábeis. Além disso, foram desenvolvidas queries analíticas para extrair informações relevantes sobre despesas das operadoras.

## Estrutura do Projeto
O projeto é composto pelos seguintes arquivos:

- `scripts/01_setup.sql` - Criação do schema e tabelas.
- `scripts/02_import.sql` - Importação dos dados.
- `scripts/03_analytics.sql` - Consultas analíticas.
- `docker-compose.yml` - Configuração do ambiente Docker para PostgreSQL e PgAdmin.

## Configuração do Ambiente
Este projeto utiliza Docker para facilitar a implantação do banco de dados. Certifique-se de ter o Docker e o Docker Compose instalados.

### Passos para Configuração
1. **Clonar o repositório**:
   ```sh
   git clone https://github.com/seu-repositorio.git
   cd seu-repositorio
   ```

2. **Baixar os arquivos de dados**:
   - Demonstrativos Contábeis: [ANS Dados Abertos](https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/)
   - Dados cadastrais das Operadoras: [ANS Operadoras Ativas](https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/)

   Salve os arquivos CSV na pasta `database/data/`.

3. **Subir o ambiente Docker**:
   ```sh
   docker-compose up -d
   ```

4. **Acessar o PgAdmin**:
   - URL: [http://localhost:5050](http://localhost:5050)
   - Usuário: `admin@ans.com`
   - Senha: `admin123`

5. **Executar os scripts SQL**:
   - Acesse o container PostgreSQL:
     ```sh
     docker exec -it ans_postgres bash
     ```
   - Conecte-se ao banco:
     ```sh
     psql -U ans_admin -d ans_db
     ```
   - Execute os scripts:
     ```sql
     \i /scripts/01_setup.sql;
     \i /scripts/02_import.sql;
     \i /scripts/03_analytics.sql;
     ```

## Estrutura do Banco de Dados
### Schema: `ans`

#### Tabela: `operadoras`
| Campo | Tipo | Descrição |
|--------|------|------------|
| `registro_ans` | VARCHAR(6) | Identificador único da operadora |
| `cnpj` | VARCHAR(14) | CNPJ da operadora |
| `razao_social` | VARCHAR(255) | Nome da empresa |
| `nome_social` | VARCHAR(255) | Nome social |
| `modalidade` | VARCHAR(200) | Tipo de operadora |
| `logradouro` | VARCHAR(255) | Endereço |
| `numero` | VARCHAR(30) | Número |
| `complemento` | VARCHAR(200) | Complemento |
| `bairro` | VARCHAR(100) | Bairro |
| `cidade` | VARCHAR(100) | Cidade |
| `uf` | CHAR(2) | Estado |
| `cep` | VARCHAR(8) | CEP |
| `ddd` | VARCHAR(2) | DDD |
| `telefone` | VARCHAR(20) | Telefone |
| `fax` | VARCHAR(15) | Fax |
| `endereco_eletronico` | VARCHAR(100) | E-mail |
| `representante` | VARCHAR(255) | Nome do representante |
| `cargo_representante` | VARCHAR(100) | Cargo do representante |
| `regiao_de_comercializacao` | VARCHAR(255) | Região de atuação |
| `data_registro_ans` | DATE | Data do registro |

#### Tabela: `demonstracoes`
| Campo | Tipo | Descrição |
|--------|------|------------|
| `id` | SERIAL | Identificador único |
| `registro_ans` | VARCHAR(6) | Identificador da operadora |
| `data` | DATE | Data do registro |
| `cd_conta_contabil` | VARCHAR(200) | Código da conta contábil |
| `descricao` | VARCHAR(250) | Descrição da conta |
| `valor_saldo_inicial` | NUMERIC(15,2) | Saldo inicial |
| `valor_saldo_final` | NUMERIC(15,2) | Saldo final |

## Consultas Analíticas

### 1. Top 10 Operadoras com Maiores Despesas no Último Trimestre
```sql
SELECT
    o.razao_social AS "RAZÃO SOCIAL",
    COALESCE(o.nome_social , '') AS "NOME SOCIAL",
    o.registro_ans AS "REGISTRO ANS",
    d.descricao AS "DESCRIÇÃO",
    TO_CHAR(SUM(valor_saldo_final), 'R$ FM999,999,999,999.00') AS "TOTAL DESPESAS"
FROM
    ans.demonstracoes d
    INNER JOIN ans.operadoras o ON o.registro_ans = d.registro_ans
    INNER JOIN (
        SELECT
            DATE_TRUNC('quarter', MAX(d.data)) AS inicio,
            DATE_TRUNC('quarter', MAX(d.data)) + INTERVAL '3 months' AS fim
        FROM ans.demonstracoes d
    ) a ON d.data >= a.inicio AND d.data < a.fim
WHERE
    d.descricao LIKE '%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'
GROUP BY
    o.razao_social, o.nome_social, o.registro_ans, d.descricao
ORDER BY
    SUM(valor_saldo_final) DESC, o.razao_social
LIMIT 10;
```

### 2. Top 10 Operadoras com Maiores Despesas no Último Ano
```sql
SELECT
    o.razao_social AS "RAZÃO SOCIAL",
    COALESCE(o.nome_social , '') AS "NOME SOCIAL",
    o.registro_ans AS "REGISTRO ANS",
    d.descricao AS "DESCRIÇÃO",
    TO_CHAR(SUM(valor_saldo_final), 'R$ FM999,999,999,999.00') AS "TOTAL DESPESAS"
FROM
    ans.demonstracoes d
    INNER JOIN ans.operadoras o ON o.registro_ans = d.registro_ans
    INNER JOIN (
        SELECT
            DATE_TRUNC('year', MAX(d.data)) AS inicio,
            DATE_TRUNC('year', MAX(d.data)) + INTERVAL '1 year' AS fim
        FROM ans.demonstracoes d
    ) a ON d.data >= a.inicio AND d.data < a.fim
WHERE
    d.descricao LIKE '%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%'
GROUP BY
    o.razao_social, o.nome_social, o.registro_ans, d.descricao
ORDER BY
    SUM(valor_saldo_final) DESC, o.razao_social
LIMIT 10;
```

---
Este projeto é confidencial e não deve ser compartilhado sem autorização expressa.