from fastapi import APIRouter, Query
from typing import List
from src.Repositories.CityRepository import CityRepository
from src.Repositories.RegionRepository import RegionRepository

router = APIRouter()


@router.get("/get-cities")
def default_csv_model(state_id: List[int] = Query(...)):
    cities = CityRepository.get_all(state_id=state_id).sort_values(by=['name'])

    return {
        'message': 'Operação concluída com sucesso.',
        'data': cities.to_dict(orient='records')
    }

