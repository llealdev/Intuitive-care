from fastapi import APIRouter, HTTPException
from ..service.csv_service import CSVService
import json

router = APIRouter()
csv_service = CSVService()

@router.get("/operadoras")
async def buscar_operadoras(q: str = "", limit: int = 50):
    try:
        results = csv_service.search_operadoras(search_term=q, max_results=limit)
        
        # Limpeza adicional para garantir compatibilidade com JSON
        def clean_data(data):
            if isinstance(data, dict):
                return {k: clean_data(v) for k, v in data.items()}
            elif isinstance(data, (list, tuple)):
                return [clean_data(item) for item in data]
            elif isinstance(data, (int, str, bool)) or data is None:
                return data
            else:
                return str(data)
        
        cleaned_results = clean_data(results)
        
        return {
            "success": True,
            "count": len(results),
            "results": cleaned_results
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar a requisição: {str(e)}"
        )