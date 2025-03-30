--CRIANDO SCHEMA DO BANCO DE DADOS
CREATE SCHEMA IF NOT EXISTS ans;

--Tabela de operadoras ativas
CREATE TABLE ans.operadoras(
	registro_ans VARCHAR(6) PRIMARY KEY,
	cnpj VARCHAR(14) NOT NULL,
	razao_social VARCHAR(255) NOT NULL,
	nome_social VARCHAR(255),
	modalidade VARCHAR(200),
	logradouro VARCHAR(255),
	numero VARCHAR(30),
	complemento VARCHAR(200),
	bairro VARCHAR(100),
	cidade VARCHAR(100),
	uf CHAR(2),
	cep VARCHAR(8),
	ddd VARCHAR(2),
	telefone VARCHAR(20),
	fax VARCHAR(15),
	endereco_eletronico VARCHAR(100),
	representante VARCHAR(255),
	cargo_representante VARCHAR(100),
	regiao_de_comercializacao VARCHAR(255),
	data_registro_ans DATE
	
);

--Tabela de demonstrações contábeis
CREATE TABLE ans.demonstracoes (
	id SERIAL PRIMARY KEY,
	registro_ans VARCHAR(6),
	DATA DATE NOT NULL,
	cd_conta_contabil VARCHAR(200) NOT NULL,
	descricao varchar(250) NOT NULL,
    valor_saldo_inicial NUMERIC(15,2) NOT NULL,
    valor_saldo_final NUMERIC(15,2) NOT NULL
);


-- Índices para otimização
CREATE INDEX idx_demo_operadora ON ans.demonstracoes(registro_ans);
CREATE INDEX idx_demo_periodo ON ans.demonstracoes(DATA);
CREATE INDEX idx_demo_conta ON ans.demonstracoes(CD_CONTA_CONTABIL);


