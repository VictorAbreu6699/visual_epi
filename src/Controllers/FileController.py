from fastapi import APIRouter
from fastapi.responses import FileResponse
from src.Services.XLSXService import XLSXService
import os

router = APIRouter()


@router.get("/default-xlsx-model")
def default_csv_model():
    file_path = XLSXService.generate_default_file()
    return FileResponse(path=file_path, filename=os.path.basename(file_path), media_type='text/csv')

