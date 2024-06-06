import datetime
import uuid

from pydantic import BaseModel


# Схемы для добавления записи в базу данных

class AddHotelSchema(BaseModel):
    name: str
    address: str


class AddRoomSchema(BaseModel):
    hotel_id: uuid.UUID
    room_number: str
    price: float


class AddRentSchema(BaseModel):
    id_user: uuid.UUID
    room_id: uuid.UUID


class UpdateRentSchema(AddRentSchema):
    data_rent: datetime.datetime


class AuthSchema(BaseModel):
    email: str
    password: str


class RegUserSchema(AuthSchema):
    first_name: str
    last_name: str
    surname: str
