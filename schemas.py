import datetime
import uuid
from typing import Optional
from enum import Enum
from pydantic import BaseModel


# Схемы для добавления записи в базу данных

class CleaningFrequency(str, Enum):
    none = "Нет"
    daily = "Раз в день"
    weekly = "Раз в неделю"


class ParkingAvailability(str, Enum):
    yes = "Да"
    no = "Нет"


class AddHotelSchema(BaseModel):
    name: str
    address: str
    city_center_distance: float  # Близость к центру города
    cleaning_frequency: CleaningFrequency  # Наличие уборки
    parking_availability: ParkingAvailability  # Наличие парковки


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
