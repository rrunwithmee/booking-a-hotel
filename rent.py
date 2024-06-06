import uuid
from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from DataBase_def import create_rent, get_room, get_all_rents, get_rent_by_id, delete_rent, update_rent, get_user_by_id
from schemas import AddRentSchema, UpdateRentSchema

router = APIRouter(prefix='/rent',
                   tags=['rent'],
                   responses={404: {"description": "Not found"}})


@router.post('/add_rent')
def add_rent_rout(data: AddRentSchema):
    if get_user_by_id(data.id_user) is None:
        return HTTPException(status_code=400, detail="User not found")

    if get_room(data.room_id) is None:
        return HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='No such Room')

    if create_rent(data.id_user, data.room_id):
        return HTTPException(status_code=HTTPStatus.OK)

    return HTTPException(status_code=401, detail="This room is already rented")



@router.get('/all')
def get_all_rents_rout():
    return get_all_rents()


@router.get('/{rent_id}')
def get_rent_rout(rent_id: uuid.UUID):
    rent = get_rent_by_id(rent_id)

    if rent is not None:
        return rent
    return HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='No such Rent')


@router.delete('/{rent_id}')
def delete_rent_rout(rent_id: uuid.UUID):
    delete_rent(rent_id)
    return HTTPException(status_code=HTTPStatus.OK, detail='Rent Deleted')


@router.put('/{rent_id}')
def update_rent_rout(rent_id: uuid.UUID, data: UpdateRentSchema):
    rent = get_rent_by_id(rent_id)
    if rent is not None:
        update_rent(rent_id, data.dict())
        return HTTPException(status_code=HTTPStatus.OK)
    return HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='No such Rent')
