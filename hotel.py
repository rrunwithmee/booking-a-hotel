import uuid

from fastapi import APIRouter

from DataBase_def import create_hotel, get_hotels, get_hotel_by_id, delete_hotel_by_id, update_hotel_by_id
from schemas import AddHotelSchema

router = APIRouter(prefix='/hotel',
                   tags=['hotel'],
                   responses={404: {"description": "Not found"}})


@router.post('/add_hotel')
def add_hotel(data: AddHotelSchema):
    create_hotel(data.name, data.address)


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

# from fastapi import APIRouter, Request
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
#
# from DataBase_def import create_hotel, get_hotels, get_hotel_by_id, delete_hotel_by_id, update_hotel_by_id
# from schemas import AddHotelSchema
#
# router = APIRouter(prefix='/hotel',
#                    tags=['hotel'],
#                    responses={404: {"description": "Not found"}})
#
# templates = Jinja2Templates(directory="templates")
#
# @router.post('/add_hotel', response_class=HTMLResponse)
# async def add_hotel(request: Request, data: AddHotelSchema):
#     create_hotel(data.name, data.address)
#     return templates.TemplateResponse("lenta.html", {"request": request})
#
# @router.get('/all', response_class=HTMLResponse)
# async def get_all_hotels(request: Request):
#     hotels = get_hotels()
#     return templates.TemplateResponse("all_hotels.html", {"request": request, "hotels": hotels})
#
# @router.get('/{hotel_id:uuid}', response_class=HTMLResponse)
# async def get_hotel(request: Request, hotel_id: uuid.UUID):
#     hotel = get_hotel_by_id(hotel_id)
#     return templates.TemplateResponse("hotel_details.html", {"request": request, "hotel": hotel})
#
# @router.put('/{hotel_id:uuid}', response_class=HTMLResponse)
# async def update_hotel(request: Request, hotel_id: uuid.UUID, data: AddHotelSchema):
#     update_hotel_by_id(hotel_id, data.dict())
#     return templates.TemplateResponse("lenta.html", {"request": request})
#
# @router.delete('/{hotel_id:uuid}', response_class=HTMLResponse)
# async def delete_hotel(request: Request, hotel_id: uuid.UUID):
#     delete_hotel_by_id(hotel_id)
#     return templates.TemplateResponse("lenta.html", {"request": request})
