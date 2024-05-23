from fastapi import APIRouter

from src.Repositories.CityRepository import CityRepository
from src.Repositories.RegionRepository import RegionRepository

router = APIRouter()


@router.get("/get-cities")
def default_csv_model():
    cities = CityRepository.get_all()

    return {
        'message': 'Operação concluída com sucesso.',
        'data': cities.to_dict(orient='records')
    }

