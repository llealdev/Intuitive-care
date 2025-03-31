from pathlib import Path 

class Settings:
    
    def __init__(self):
        self.app_name = "API Operadoras"
        self.csv_path = str(Path(__file__).parent.parent / "data" / "operadoras.csv")

settings = Settings()

    