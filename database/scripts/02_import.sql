--INSERINDO DADOS

sed -i 's/,/./g' /dados/1T2023.csv
sed -i 's/,/./g' /dados/2T2023.csv
sed -i 's/,/./g' /dados/3T2023.csv
sed -i 's/,/./g' /dados/4T2023.csv
sed -i 's/,/./g' /dados/1T2024.csv
sed -i 's/,/./g' /dados/2T2024.csv
sed -i 's/,/./g' /dados/3T2024.csv
sed -i 's/,/./g' /dados/4T2024.csv

COPY ans.operadoras FROM '/dados/Relatorio_cadop.csv'
WITH CSV HEADER DELIMITER ';' ENCODING 'UTF8';

COPY ans.demonstracoes(data, registro_ans, cd_conta_contabil, descricao, valor_saldo_inicial, valor_saldo_final) 
FROM '/dados/1T2023.csv' 
WITH CSV HEADER DELIMITER ';' ENCODING 'UTF8';

COPY ans.demonstracoes(data, registro_ans, cd_conta_contabil, descricao, valor_saldo_inicial, valor_saldo_final) 
FROM '/dados/2T2023.csv' 
WITH CSV HEADER DELIMITER ';' ENCODING 'UTF8';

COPY ans.demonstracoes(data, registro_ans, cd_conta_contabil, descricao, valor_saldo_inicial, valor_saldo_final) 
FROM '/dados/3T2023.csv' 
WITH CSV HEADER DELIMITER ';' ENCODING 'UTF8';

COPY ans.demonstracoes(data, registro_ans, cd_conta_contabil, descricao, valor_saldo_inicial, valor_saldo_final) 
FROM '/dados/4T2023.csv' 
WITH CSV HEADER DELIMITER ';' ENCODING 'UTF8';

COPY ans.demonstracoes(data, registro_ans, cd_conta_contabil, descricao, valor_saldo_inicial, valor_saldo_final) 
FROM '/dados/1T2024.csv' 
WITH CSV HEADER DELIMITER ';' ENCODING 'UTF8';

COPY ans.demonstracoes(data, registro_ans, cd_conta_contabil, descricao, valor_saldo_inicial, valor_saldo_final) 
FROM '/dados/2T2024.csv' 
WITH CSV HEADER DELIMITER ';' ENCODING 'UTF8';

COPY ans.demonstracoes(data, registro_ans, cd_conta_contabil, descricao, valor_saldo_inicial, valor_saldo_final) 
FROM '/dados/3T2024.csv' 
WITH CSV HEADER DELIMITER ';' ENCODING 'UTF8';

COPY ans.demonstracoes(data, registro_ans, cd_conta_contabil, descricao, valor_saldo_inicial, valor_saldo_final)
 FROM '/dados/4T2024.csv' 
 WITH CSV HEADER DELIMITER ';' ENCODING 'UTF8';