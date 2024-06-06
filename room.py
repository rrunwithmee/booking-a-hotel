import uuid
from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from DataBase_def import get_all_room, add_room, get_room, delete_room, get_hotel_by_id, update_room
from schemas import AddRoomSchema

router = APIRouter(prefix='/room',
                   tags=['room'],
                   responses={404: {"description": "Not found"}})


@router.get('/all')
def get_all_room_rout():
    return get_all_room()


@router.get('/{room_id}')
def get_room_by_id(room_id: uuid.UUID):
    room = get_room(room_id)
    if room is None:
        return HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Room not found")
    return room


@router.post('/add_room')
def add_room_rout(data: AddRoomSchema):
    if get_hotel_by_id(data.hotel_id) is not None:
        add_room(data.hotel_id, data.room_number, data.price)
        return HTTPException(status_code=HTTPStatus.OK)
    return HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='No such Hotel')


@router.delete('/{room_id}')
def delete_room_rout(room_id: uuid.UUID):
    delete_room(room_id)
    return HTTPException(status_code=HTTPStatus.OK, detail='Room deleted')


@router.put('/{room_id}')
def update_room_rout(room_id: uuid.UUID, data: AddRoomSchema):
    if get_hotel_by_id(data.hotel_id) is not None:
        update_room(room_id, data.dict())
        return HTTPException(status_code=HTTPStatus.OK)
    return HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='No such Hotel')
