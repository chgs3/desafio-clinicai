from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import endpoints

app = FastAPI(
    title = "ClinicAI Agent API",
    description = "API para interagir com o agente de triagem da ClinicAI."
)

origins = [
    "null",
    "http://127.0.0.1",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

# Config do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# rotas da API
app.include_router(endpoints.router)