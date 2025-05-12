from fastapi import FastAPI
from routes.api import api_router

app = FastAPI()
app.title = "Prueba Tecnica FastAPI"
app.version = "1.0"

app.include_router(api_router)