from fastapi import APIRouter, Request, Depends, responses, status
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from DataBase_model import Hotel, User, Room
from crypto import hash_password, create_jwt_token
from DataBase_def import db_session
from starlette.responses import RedirectResponse

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

    # if password is None:
    #     errors.append("Пароль не может быть пустым!")
    # else:
    #     if len(password) < 6:
    #         errors.append("Пароль должен состоять от 6 и более символов!")
    #         return templates.TemplateResponse("reg.html", {"request": request, "errors": errors})
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
