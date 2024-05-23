from fastapi import APIRouter
from src.Repositories.StateRepository import StateRepository

router = APIRouter()


@router.get("/get-states")
def default_csv_model():
    states = StateRepository.get_all()

    return {
        'message': 'Operação concluída com sucesso.',
        'data': states.to_dict(orient='records')
    }

