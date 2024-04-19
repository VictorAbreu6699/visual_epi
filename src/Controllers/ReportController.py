from datetime import datetime
from tempfile import NamedTemporaryFile

import pandas as pd
from fastapi import APIRouter, Query, UploadFile, File, HTTPException
from typing import List

from src.Repositories.SicknessReportRepository import SicknessReportRepository
from src.Services.XLSXService import XLSXService

router = APIRouter()


@router.get("/report-sickness")
def report(
        start_date: datetime, end_date: datetime,
        sickness_id: List[int] = Query(None), city_id: List[int] = Query(None), state_id: List[int] = Query(None)
):
    df_sickness_report = SicknessReportRepository.get_all(
        sickness_id=sickness_id, city_id=city_id, state_id=state_id,
        start_date=start_date, end_date=end_date
    )

    return {
        "message": "Operação concluída com sucesso.",
        "data": df_sickness_report.to_dict(orient='records')
    }


@router.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    # Verifica se o arquivo é um Excel
    if not file.filename.endswith('.xlsx'):
        raise HTTPException(
            status_code=400, detail="Formato de arquivo inválido. Apenas arquivos Excel (.xlsx) são permitidos."
        )

    try:
        # Salva o arquivo temporariamente
        with NamedTemporaryFile(delete=False) as tmp:
            tmp.write(await file.read())
            tmp.flush()
            tmp.seek(0)

            XLSXService.import_file_to_database(tmp.name)

        return {"message": "Arquivo recebido e importado com sucesso."}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ocorreu um erro ao processar o arquivo: {}".format(str(e)))
