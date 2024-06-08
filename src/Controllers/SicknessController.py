from fastapi import APIRouter, Query
from typing import List
from src.Repositories.CityRepository import CityRepository
from src.Repositories.RegionRepository import RegionRepository
from src.Repositories.SicknessRepository import SicknessRepository

router = APIRouter()


@router.get("/get-sickness")
def default_csv_model():
    sickness = SicknessRepository.get_all().sort_values(by=['name'])

    return {
        'message': 'Operação concluída com sucesso.',
        'data': sickness.to_dict(orient='records')
    }

