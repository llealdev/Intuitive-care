import pandas as pd 

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
        Realiza a limpeza e transformação dos dados:
        - Padroniza cabeçalhos
        - Substitui abreviações
        - Remove caracteres especiais
    """

    #Define os cabeçalhos corretos
    columns = [
        "PROCEDIMENTO",
        "RN_ALTERACAO",
        "VIGÊNCIA",
        "OD",
        "AMB",
        "HCO",
        "HSO",
        "REF",
        "PAC",
        "DUT",
        "SUBGRUPO",
        "GRUPO",
        "CAPÍTULO"
    ]

    # Verifica se o número de colunas coincide
    if len(df.columns) != len(columns):
        raise ValueError(f"Número de colunas incompatível. Esperado: {len(columns)}, Encontrado: {len(df.columns)}")
    
    df.columns = columns

    # Substitui abreviações conforme a legenda
    replacements = {
        "OD": {"OD": "Odontológico"},
        "AMB": {"AMB": "Ambulatorial"},
        "HCO": {"HCO": "Hospitalar com Obstetrícia"},
        "HSO": {"HSO": "Hospitalar sem Obstetrícia"},
        "REF": {"REF": "Plano Referência"},
        "PAC": {"PAC": "Procedimento de Alta Complexidade"},
        "DUT": {"DUT": "Diretriz de Utilização"}
    }

    for col in ["OD", "AMB", "HCO", "HSO", "REF", "PAC", "DUT"]:
        if col in df.columns:
            df[col] = df[col].replace(replacements[col])

    # Limpeza adicional
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].str.strip()

    return df 