from fastapi import APIRouter
from src.Repositories.RegionRepository import RegionRepository

router = APIRouter()


@router.get("/get-regions")
def default_csv_model():
    regions = RegionRepository.get_all()

    return {
        'message': 'Operação concluída com sucesso.',
        'data': regions.to_dict(orient='records')
    }

