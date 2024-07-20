import uuid
from passlib.hash import pbkdf2_sha256
import datetime

from fastapi import HTTPException, Response
from sqlalchemy import delete, update

from DataBase_model import User, Room, engine, Hotel, Rent
from sqlmodel import Session, select


def get_users():
    with Session(engine) as session:
        return session.exec(select(User)).all()


def get_user_by_email(email: str):
    with Session(engine) as session:
        return session.exec(select(User).where(User.email == email)).first()


def get_user_by_id(user_id: uuid.UUID):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.id == user_id)).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user


def delete_user(user_id: uuid.UUID):
    with Session(engine) as session:
        session.exec(delete(User).where(User.id == user_id))
        session.commit()


def reg_user(email: str,
             password: str,
             first_name: str,
             last_name: str,
             surname: str, ):
    user = User(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        surname=surname
    )
    with Session(engine) as session:
        if session.exec(select(User).where(User.email == email)).first() is None:
            session.add(user)
            session.commit()
            return True
        else:
            return False


def create_hotel(name: str, address: str, city_center_distance: float, cleaning_frequency: str, parking_availability: str):
    hotel = Hotel(
        name=name,
        address=address,
        city_center_distance=city_center_distance,
        cleaning_frequency=cleaning_frequency,
        parking_availability=parking_availability
    )

    with Session(engine) as session:
        session.add(hotel)
        session.commit()


def get_hotels():
    with Session(engine) as session:
        return session.exec(select(Hotel)).all()


def get_hotel_by_id(hotel_id: uuid.UUID):
    with Session(engine) as session:
        return session.exec(select(Hotel).where(Hotel.id == hotel_id)).first()


def update_hotel_by_id(hotel_id: uuid.UUID, data: dict):
    with Session(engine) as session:
        hotel = session.exec(select(Hotel).where(Hotel.id == hotel_id)).first()

        if not hotel:
            raise HTTPException(status_code=404, detail="Hotel not found")

        hotel.name = data.get('name', hotel.name)
        hotel.address = data.get('address', hotel.address)
        hotel.city_center_distance = data.get('city_center_distance', hotel.city_center_distance)
        hotel.cleaning_frequency = data.get('cleaning_frequency', hotel.cleaning_frequency)
        hotel.parking_availability = data.get('parking_availability', hotel.parking_availability)

        session.commit()


def delete_hotel_by_id(hotel_id: uuid.UUID):
    with Session(engine) as session:
        session.exec(delete(Hotel).where(Hotel.id == hotel_id))
        session.commit()


def get_all_room():
    with Session(engine) as session:
        return session.exec(select(Room)).all()


def get_room(room_id: uuid.UUID):
    with Session(engine) as session:
        return session.exec(select(Room).where(Room.id == room_id)).first()


def add_room(hotel_id: uuid.UUID,
             room_number: str,
             price: float):
    room = Room(
        hotel_id=hotel_id,
        room_number=room_number,
        price=price
    )

    with Session(engine) as session:
        session.add(room)
        session.commit()


def delete_room(room_id: uuid.UUID):
    with Session(engine) as session:
        session.exec(delete(Room).where(Room.id == room_id))
        session.commit()


def update_room(room_id: uuid.UUID, data: dict):
    with Session(engine) as session:
        room = session.exec(select(Room).where(Room.id == room_id)).first()

        room.hotel_id = data['hotel_id']
        room.room_number = data['room_number']
        room.price = data['price']

        session.commit()




def create_rent(id_user: uuid.UUID, room_id: uuid.UUID):
    rent = Rent(id_user=id_user, room_id=room_id)
    with Session(engine) as session:
        if session.exec(select(Rent).where(Rent.room_id == room_id)).first() is not None:
            return False
        session.add(rent)
        session.commit()
        return True


def get_all_rents():
    with Session(engine) as session:
        return session.exec(select(Rent)).all()


def get_rent_by_id(rent_id: uuid.UUID):
    with Session(engine) as session:
        return session.exec(select(Rent).where(Rent.id == rent_id)).first()


def delete_rent(rent_id: uuid.UUID):
    with Session(engine) as session:
        session.exec(delete(Rent).where(Rent.id == rent_id))
        session.commit()


def update_rent(rent_id: uuid.UUID, data: dict):
    with Session(engine) as session:
        rent = session.exec(select(Rent).where(Rent.id == rent_id)).first()

        rent.room_id = data['room_id']
        rent.id_user = data['id_user']
        rent.data_rent = data['data_rent']

        session.commit()


def db_session():
    with Session(engine) as session:
        yield session
