from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.endpoints import router as api_router
from .config.settings import settings 

app = FastAPI(
    title="API de Operadoras",
    description="API para buscar operadoras de saúde",
    version="1.0.0"
)

# CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return{"message": "API de Operadoras está funcionando"}
 
