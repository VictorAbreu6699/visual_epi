from typing import List

from fastapi import APIRouter, Query
from src.Repositories.StateRepository import StateRepository

router = APIRouter()


@router.get("/get-states")
def default_csv_model(region_id: List[int] = Query(...)):
    states = StateRepository.get_all(region_id=region_id).sort_values(by=['name'])

    return {
        'message': 'Operação concluída com sucesso.',
        'data': states.to_dict(orient='records')
    }

