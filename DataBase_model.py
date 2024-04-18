import datetime
from sqlmodel import Field, SQLModel, create_engine, Relationship, UniqueConstraint
import uuid


class User(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("email"),)

    id: uuid.UUID = Field(primary_key=True, default=None)
    password: str = Field(min_length=64, max_length=64)  # хэш пароля
    email: str  # почта
    first_name: str  # имя
    last_name: str  # отчество
    surname: str  # фамилия
    date_reg: datetime.datetime  # дата регистрации

    rents: list['Rent'] = Relationship(back_populates='users')
    payments: list['Payment'] = Relationship(back_populates='users')


class Room(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("room_number"),)

    id: uuid.UUID = Field(primary_key=True, default=None)
    hotel: str  # отель
    room_number: str  # номер комнаты
    price: int  # цена аренды

    rents: list['Rent'] = Relationship(back_populates='rooms')


class Rent(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True, default=None)
    id_user: uuid.UUID = Field(default=None, foreign_key='user.id')  # id_пользователя
    room_id: uuid.UUID = Field(default=None, foreign_key='room.id')
    floor: int
    data_rent: datetime.datetime  # дата аренды

    users: list['User'] = Relationship(back_populates='rents')
    payments: list['Payment'] = Relationship(back_populates='rents')
    rooms: list['Room'] = Relationship(back_populates='rents')


class Payment(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True, default=None)
    id_rent: uuid.UUID = Field(default=None, foreign_key='rent.id')  # id аренды
    id_user: uuid.UUID = Field(default=None, foreign_key='user.id')  # id пользователя
    last_cart_num: int  # последние 4 цифры карты
    data: datetime.datetime  # дата оплаты

    rents: list['Rent'] = Relationship(back_populates='payments')
    users: list['User'] = Relationship(back_populates='payments')


class UserUpdate(SQLModel):
    email: str
    password: str


sqlite_file_name = "../database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url)

