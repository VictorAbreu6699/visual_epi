from fastapi import FastAPI
from src.Controllers import HomeController, FileController, ReportController

app = FastAPI()

# Adiciona os routers dos controladores à aplicação
app.include_router(HomeController.router)
app.include_router(FileController.router)
app.include_router(ReportController.router)
