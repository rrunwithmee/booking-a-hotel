import datetime

from sqlmodel import Field, SQLModel, create_engine, UniqueConstraint
import uuid
from sqlmodel import Session




class User(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("email"), UniqueConstraint("id"))

    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    password: str = Field(min_length=64, max_length=64)  # хэш пароля
    email: str = Field(nullable=False)  # почта
    first_name: str  # имя
    last_name: str  # отчество
    surname: str  # фамилия
    date_reg: datetime.datetime = Field(default_factory=datetime.datetime.now)  # дата регистрации


class Hotel(SQLModel, table=True):
    __table_args__ = (UniqueConstraint('id'),)

    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    name: str = Field(nullable=False)
    address: str = Field(nullable=False)


class Room(SQLModel, table=True):
    __table_args__ = (UniqueConstraint('id'),)

    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4, nullable=False)
    hotel_id: uuid.UUID = Field(foreign_key='hotel.id', nullable=False)  # отель
    room_number: str = Field(nullable=False)  # номер комнаты
    price: float = Field(nullable=False)  # цена аренды


class Rent(SQLModel, table=True):
    __table_args__ = (UniqueConstraint('id'), )

    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4, nullable=False)
    id_user: uuid.UUID = Field(foreign_key='user.id', nullable=False)  # id_пользователя
    room_id: uuid.UUID = Field(foreign_key='room.id', nullable=False)
    data_rent: datetime.datetime = Field(nullable=False, default_factory=datetime.datetime.now)  # дата аренды


class UserUpdate(SQLModel):
    email: str
    password: str


sqlite_file_name = "./database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url)












# SQLModel.metadata.create_all(engine)  # Создать базу данных и таблицы в ней (Нужно раскоментировать строку и запустить этот файл)
