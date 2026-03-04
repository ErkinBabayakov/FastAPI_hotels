from fastapi import APIRouter, Body
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest, BookingAdd


router = APIRouter(prefix="/bookings", tags=["Бронирование номера"])

@router.post("", summary="Добавить бронирование")
async def add_booking(db: DBDep,
                      user_id: UserIdDep,
                      booking_data: BookingAddRequest = Body()):
    #Получаем цену номера
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price: int = room.price
    #Создаем схему данных BooingAdd
    _booking_data = BookingAdd(user_id=user_id, price=room_price, **booking_data.model_dump())
    #Добавляем бронирование конкретному пользователю
    data = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": data}