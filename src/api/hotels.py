from fastapi import Query, APIRouter, Body
from src.api.dependencies import PaginationDep
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get("", summary="Получить данные об отеле")
def get_hotel(
        pagination: PaginationDep,
        id: int | None = Query(None, description="Айди"),
        title: str | None = Query(default=None, description="Отель")
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_[pagination.per_page * (pagination.page - 1):][:pagination.per_page]


@router.delete("/hotel_id", summary="Удаляем отель")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"OK": 200}

@router.post("", summary="Создаем отель")
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "Отель Сочи 5 звезд у моря",
        "name": "sochi_u_morya"
    }},
    "2": {"summary": "Дубай", "value": {
        "title": "Отель Дубай у Бурдж-Халиф",
        "name": "dubay_u_burj_chalifa"
    }}
})):
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
def partial_update_hotel(hotel_id: int, hotel_data: HotelPATCH):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.name:
        hotel["name"] = hotel_data.name
    return {"status": 200}