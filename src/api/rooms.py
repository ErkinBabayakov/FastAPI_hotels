from fastapi import APIRouter, Body
from src.database import async_session_maker
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest
from src.repositories.rooms import RoomsRepository

router = APIRouter(prefix="/hotels", tags=["Номера отелей"])

@router.get("/{hotel_id}/rooms", summary="Получить все номера отеля")
async def get_rooms(hotel_id:int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_filtered(hotel_id=hotel_id)

@router.get("/{hotel_id}/rooms{room_id}", summary="Получить номер отеля")
async def get_rooms(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(hotel_id=hotel_id, id=room_id)


@router.post("/{hotel_id}/rooms", summary="Создать номер отеля")
async def create_room(hotel_id: int ,room_data: RoomAddRequest = Body()):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(_room_data)
        await session.commit()
    return {"status": "OK", "data": room}

@router.put("/{hotel_id}/rooms", summary="Обновить информацию о номере")
async def update_room(hotel_id:int, room_id:int, room_data: RoomAddRequest):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, hotel_id=hotel_id, id=room_id)
        await session.commit()
    return {"status": "OK"}

@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частично обновить информацию о номере")
async def partial_update_room(hotel_id:int, room_id:int, room_data: RoomPatchRequest):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_none=True))
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status": "OK"}

@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удалить номер в отеле")
async def delete_room(hotel_id:int, room_id:int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(hotel_id=hotel_id ,id=room_id)
        await session.commit()
        return {"status": "OK"}