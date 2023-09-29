from fastapi import FastAPI
from router.router import user
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(user)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200/"],  # Cambia "*" a la URL de tu frontend en producción
    allow_methods=["*"],
    allow_headers=["*"],
)