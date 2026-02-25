from fastapi import Body, Query, APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/hotels", tags=["Отели"])

class Hotel(BaseModel):
    title: str
    name: str

hotels = [
    {"id": 1, "title": "Sochi", "name": "Красная поляна"},
    {"id": 2, "title": "Дубай", "name": "Бурж-Халифа"}
]

@router.get("/get_hotels", summary="Получить данные об отелях")
def get_hotels():
    return hotels

@router.get("", summary="Получить данные об отеле")
def get_hotel(id: int | None = Query(None, description="Айди"),
              title: str | None = Query(default=None, description="Отель"),
              ):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_

@router.delete("/hotel_id", summary="Удаляем отель")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"OK": 200}

@router.post("", summary="Создаем отель")
def create_hotel(hotel_data: Hotel):
    global hotels
    hotels.append({"id": hotels[-1]["id"] + 1,
                  "title": hotel_data.title,
                   "name": hotel_data.name,})
    return {"status": "OK"}

@router.put("/{hotel_id}", summary="Полное обновление информации об отеле")
def update_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["name"] = hotel_data.name
    hotel["title"] = hotel_data.title
    return {"status": "OK"}

@router.patch("{hotel_id}", summary="Частичное обновление информации об отеле")
def partial_update_hotel(hotel_id: int, title: str | None = Body(None), name: str | None = Body(None)):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if title:
        hotel["title"] = title
    if name:
        hotel["name"] = name
    return {"status": 200}