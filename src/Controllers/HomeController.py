from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="src/Templates")


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )

@router.get("/2")
def home(request: Request):
    return templates.TemplateResponse(
        request=request, name="index2.html"
    )