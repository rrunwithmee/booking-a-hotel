import uuid

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from DataBase_def import get_users, get_temp_users, get_user, check_user, delete_user, reg_user, verify_user, \
    update_user_email, update_user_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(prefix='/user',
                   tags=['user'],
                   responses={404: {"description": "Not found"}})


@router.get('/all')
def get_users_rout():
    return get_users()


@router.get('/temp_users')
def get_temp_users_rout():
    return get_temp_users()


@router.get('/{user_id}')
def get_user_rout(user_id: uuid.UUID):
    return get_user(user_id)


@router.post('/sing_in')
def check_user_rout(email: str, password: str):
    return check_user(email, password)


@router.delete('/del/')
def delete_user_rout(user_id: uuid.UUID):
    return delete_user(user_id)


@router.post('/reg')
def reg_user_rout(email: str,
             password: str,
             first_name: str,
             last_name: str,
             surname: str):
    return reg_user(email, password, first_name, last_name, surname)


@router.put('/verify/{user_id}')
def verify_user_rout(user_id: uuid.UUID):
    return verify_user(user_id)


@router.put('/update_email/{user_id}')
def update_user_email_rout(user_id: uuid.UUID, new_email: str, password: str):
    return update_user_email(user_id, new_email, password)


@router.put('/update_password/{user_id}')
def update_user_password_rout(user_id: uuid.UUID, email: str, new_password: str, new_password2: str):
    return update_user_password(user_id, email, new_password, new_password2)

