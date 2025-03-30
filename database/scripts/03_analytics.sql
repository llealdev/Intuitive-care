- ANALYTICS

-- 1. Top 10 operadoras com maiores despesas no último trimestre
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
group by 
	o.razao_social,
	o.nome_social,
	o.registro_ans,
	d.descricao
ORDER BY 
	SUM(valor_saldo_final) DESC,
	o.razao_social
limit 10;

-- 2. Top 10 operadoras com maiores despesas no último ano
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
group by 
	o.razao_social,
	o.nome_social,
	o.registro_ans,
	d.descricao
ORDER BY 
	SUM(valor_saldo_final) DESC,
	o.razao_social
limit 10;