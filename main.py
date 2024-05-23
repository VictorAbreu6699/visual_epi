from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from src.Controllers import HomeController, FileController, ReportController, RegionController, StateController, \
    CityController

app = FastAPI()

# Configuração do diretório estático
app.mount("/static", StaticFiles(directory="src/Templates"), name="static")

# Adiciona os routers dos controladores à aplicação
app.include_router(HomeController.router)
app.include_router(FileController.router)
app.include_router(ReportController.router)
app.include_router(RegionController.router)
app.include_router(StateController.router)
app.include_router(CityController.router)
