from fastapi import APIRouter, Request, Depends, responses, status
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from DataBase_model import Hotel, User, Room, Rent, engine
from crypto import hash_password, create_jwt_token, decode_jwt_token
from DataBase_def import db_session
from starlette.responses import RedirectResponse
from schemas import AddRentSchema
from DataBase_def import create_rent
import datetime
import uuid

router = APIRouter()

templates = Jinja2Templates(directory='templates')


@router.get("/")
def home_auth(request: Request, db: Session=Depends(db_session)):
    hotels = db.query(Hotel).all()
    rooms = db.query(Room).all()
    return templates.TemplateResponse("home.html", {"request": request, "hotels": hotels, "rooms": rooms})



@router.get("/reg")
def reg(request: Request):
    return templates.TemplateResponse("reg.html", {"request": request})

@router.post("/reg")
async def reg(request: Request, db: Session = Depends(db_session)):
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    first_name = form.get("first_name")
    last_name = form.get("last_name")
    surname = form.get("surname")
    errors = []

    if len(password) < 6:
        errors.append("Пароль должен состоять от 6 и более символов!")
        return templates.TemplateResponse("reg.html", {"request": request, "errors": errors})

    user = User(email=email,
                password=hash_password(password=password),
                first_name=first_name,
                last_name=last_name,
                surname=surname
                )

    duplicate_email = db.exec(select(User).where(User.email == email)).first()
    if duplicate_email:
        errors.append("Почта уже существует!")
        return templates.TemplateResponse("reg.html", {"request": request, "errors": errors})

    db.add(user)
    db.commit()
    db.refresh(user)
    msg = 'Вы зарегистрированы! Войдите в аккуанут!'
    return templates.TemplateResponse('reg.html', {"request": request, "msg": msg})






@router.get('/auth')
def auth(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})

@router.post("/auth")
async def auth(request: Request, db: Session = Depends(db_session)):
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    errors = []
    if len(password) < 6:
        errors.append("Пароль должен состоять от 6 и более символов!")
        return templates.TemplateResponse("auth.html", {"request": request, "errors": errors})
    access_token = request.cookies.get("access_token")
    if access_token:
        return RedirectResponse(url="/rent", status_code=302)
    user = db.exec(select(User).where(User.email == email)).first()
    if not user or not user.verify_password(password):
        errors.append("Неверны почта или пароль!")
        return templates.TemplateResponse("auth.html", {"request": request, "errors": errors})

    access_token = create_jwt_token(data={"sub": str(user.id)})
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return response

@router.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie(key="access_token")
    return response


@router.get("/rent")
def reg(request: Request):
    return templates.TemplateResponse("rent.html", {"request": request})

@router.post('/rent')
async def rent(request: Request, db: Session = Depends(db_session)):
    form = await request.form()
    name = form.get('name')
    room_number = form.get('room_number')
    errors = []

    access_token = request.cookies.get("access_token")
    if not access_token:
        errors.append('Войдите')
        return templates.TemplateResponse("rent.html", {"request": request, "errors": errors})
    else:
        decoded_token = decode_jwt_token('access_token')
        if decoded_token is None:
            errors.append("Неверный токен")
            return templates.TemplateResponse("rent.html", {"request": request, "errors": errors})
        email = decoded_token.get("email")
        user = db.exec(select(User).where(User.email == email)).first()
        hotel_id = db.exec(select(Hotel).where(Hotel.name == name)).first()
        room_number = db.exec(select(Room).where(Room.hotel_id == hotel_id.id, Room.room_number == room_number)).first()
        if user is None:
            errors.append('Пользователь не найден!')
            return templates.TemplateResponse("rent.html", {"request": request, "errors": errors})
        if hotel_id is None:
            errors.append('Отель не найден!')
            return templates.TemplateResponse("rent.html", {"request": request, "errors": errors})
        if room_number is None:
            errors.append('Номер не найден!')
            return templates.TemplateResponse("rent.html", {"request": request, "errors": errors})
        rent = db.exec(select(Rent).where(Rent.room_id == room_number.id)).first()
        if rent:
            errors.append('Номер уже забронирован!')
            return templates.TemplateResponse("rent.html", {"request": request, "errors": errors})
        rent = Rent(id_user=user.id, room_id=room_number.id)
        db.add(rent)
        db.commit()
        msg = 'Вы забронировали!'
        return templates.TemplateResponse('rent.html', {"request": request, "msg": msg})





# @router.post('/rent')
# async def rent(request: Request, db: Session = Depends(db_session)):
#     form = await request.form()
#     name = form.get('name')
#     room_number = form.get('room_number')
#     errors = []
#
#     access_token = request.cookies.get("access_token")
#     if access_token:
#         decoded_token = decode_jwt_token(access_token)
#         if decoded_token:
#             email = decoded_token.get("email")
#             user = db.exec(select(User).where(User.email == email)).first()
#             hotel_id = db.exec(select(Hotel).where(Hotel.name == name)).first()
#             room_number = db.exec(select(Room).where(Room.hotel_id == hotel_id.id, Room.room_number == room_number)).first()
#             if user is None:
#                 errors.append('Пользователь не найден!')
#                 return templates.TemplateResponse("rent.html", {"request": request, "errors": errors})
#             if hotel_id is None:
#                 errors.append('Отель не найден!')
#                 return templates.TemplateResponse("rent.html", {"request": request, "errors": errors})
#             if room_number is None:
#                 errors.append('Номер не найден!')
#                 return templates.TemplateResponse("rent.html", {"request": request, "errors": errors})
#             if user and hotel_id and room_number:
#                 rent = Rent(id_user=user.id, room_id=room_number.id)
#                 db.add(rent)
#                 db.commit()
#                 msg = 'Вы забронировали!'
#                 return templates.TemplateResponse('rent.html', {"request": request, "msg": msg})
#             errors.append('Комната уже забронирована!')
#             return templates.TemplateResponse("rent.html", {"request": request, "errors": errors})