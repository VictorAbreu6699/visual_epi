from fastapi import FastAPI
from src.Controllers import HomeController, FileController

app = FastAPI()

# Adiciona os routers dos controladores à aplicação
app.include_router(HomeController.router)
app.include_router(FileController.router)
