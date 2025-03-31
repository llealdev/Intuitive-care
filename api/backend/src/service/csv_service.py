import pandas as pd
from pathlib import Path
import numpy as np
from ..config.settings import settings

class CSVService:
    
    def __init__(self):
        self.df = self._load_csv()

    def _load_csv(self):
        csv_path = Path(settings.csv_path)

        if not csv_path.exists():
            raise FileNotFoundError(f"Arquivo CSV não encontrado em: {csv_path}")
        
        df = pd.read_csv(csv_path, encoding='utf-8', sep=None, engine='python')
        
        # Converter colunas relevantes para string e substituir NaN
        text_cols = ['Razao_Social', 'Nome_Fantasia', 'CNPJ']
        for col in text_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).replace('nan', '')
        
        return df

    def search_operadoras(self, search_term: str, max_results: int = 50):
        if not search_term or len(search_term) < 1:
            return []
        
        search_term = search_term.lower()
        mask = (
            self.df['Razao_Social'].str.lower().str.contains(search_term, na=False) |
            self.df['Nome_Fantasia'].str.lower().str.contains(search_term, na=False) |
            self.df['CNPJ'].str.contains(search_term, na=False)
        )

        results = self.df[mask].head(max_results)
        
        # Substituir todos os NaN/None por strings vazias antes de converter para dict
        results = results.replace({np.nan: None})
        
        return results.to_dict(orient='records')