import uuid
from fastapi import APIRouter
from DataBase_def import get_all_room, add_room, get_room, delete_room

router = APIRouter(prefix='/room',
                   tags=['room'],
                   responses={404: {"description": "Not found"}})


@router.get('/all')
def get_all_room_rout():
    return get_all_room()


@router.get('room_id}')
def get_room_rout(room_id: uuid.UUID):
    return get_room(room_id)


@router.post('/add_room')
def add_room_rout(hotel: str,
            floor: int,
            room_number: str,
            price: int):
    return add_room(hotel, floor, room_number, price)


@router.delete('/delete')
def delete_room_rout(room_id: uuid.UUID):
    return delete_room(room_id)

# @router_room.put('/update')
# def update_room(room_id: uuid.UUID):