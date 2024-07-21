import uuid

from fastapi import APIRouter

from DataBase_def import create_hotel, get_hotels, get_hotel_by_id, delete_hotel_by_id, update_hotel_by_id
from schemas import AddHotelSchema

router = APIRouter(prefix='/hotel',
                   tags=['hotel'],
                   responses={404: {"description": "Not found"}})


@router.post('/add_hotel')
def add_hotel(data: AddHotelSchema):
    # Передаем все необходимые параметры в функцию create_hotel
    create_hotel(
        name=data.name,
        address=data.address,
        star=data.star,
        city_center_distance=data.city_center_distance,
        cleaning_frequency=data.cleaning_frequency,
        parking_availability=data.parking_availability
    )


@router.get('/all')
def get_all_hotels():
    return get_hotels()


@router.get('/{hotel_id}')
def get_hotel(hotel_id: uuid.UUID):
    return get_hotel_by_id(hotel_id)


@router.put('/{hotel_id}')
def update_hotel(hotel_id: uuid.UUID, data: AddHotelSchema):
    update_hotel_by_id(hotel_id, data.dict())


@router.delete('/{hotel_id}')
def delete_hotel(hotel_id: uuid.UUID):
    delete_hotel_by_id(hotel_id)




