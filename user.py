import uuid

from fastapi import APIRouter, HTTPException, Request
from DataBase_def import get_users, get_user_by_id, delete_user, reg_user, get_user_by_email
from crypto import hash_password, create_jwt_token
from schemas import AuthSchema, RegUserSchema




router = APIRouter(prefix='/user',
                   tags=['user'],
                   responses={404: {"description": "Not found"}})









@router.get('/all')
def get_users_rout():
    return get_users()


@router.get('/{user_id}')
def get_user_rout(user_id: uuid.UUID):
    return get_user_by_id(user_id)


@router.post('/auth')
def check_user_rout(data: AuthSchema):
    user = get_user_by_email(data.email)
    if user is None:
        return HTTPException(status_code=401, detail="No user with such email")

    if hash_password(data.password) != user.password:
        return HTTPException(status_code=402, detail="Invalid password")

    return {'access_token': create_jwt_token({'user_id': str(user.id)})}

    # return {'access_token': create_jwt_token({'user_id': str(user.id), 'email': user.email})}


@router.delete('/{user_id}')
def delete_user_rout(user_id: uuid.UUID):
    return delete_user(user_id)


@router.post('/reg')
def reg_user_rout(data: RegUserSchema):
    if reg_user(data.email, hash_password(data.password), data.first_name, data.last_name, data.surname):
        return HTTPException(status_code=200, detail="User registered successfully")
    return HTTPException(status_code=400, detail="User with such email already exists")



