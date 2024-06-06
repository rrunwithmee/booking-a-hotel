from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlmodel import Session
from DataBase_model import Hotel
from DataBase_def import db_session


router = APIRouter()

templates = Jinja2Templates(directory='templates')


# @router.get('/reg', response_class=HTMLResponse)
# def get_reg_page(request: Request):
#     return templates.TemplateResponse('lenta.html', {'request': request})


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@router.get("/reg")
def reg(request: Request):
    return templates.TemplateResponse("reg.html", {"request": request})

@router.get('/auth')
def auth(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})


@router.get("/")
def home(request: Request, db: Session=Depends(db_session)):
    hotels = db.query(Hotel).all()
    return templates.TemplateResponse("home.html", {"request": request, "hotels": hotels})