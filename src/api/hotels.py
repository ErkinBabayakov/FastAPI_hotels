from fastapi import Query, APIRouter, Body
from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPATCH
from sqlalchemy import insert, select

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Получить данные об отеле")
async def get_hotel(
        pagination: PaginationDep,
        location: str | None = Query(None, description="Локация"),
        title: str | None = Query(default=None, description="Отель")
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )





@router.delete("/hotel_id", summary="Удаляем отель")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"OK": 200}

@router.post("", summary="Создаем отель")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {""
          "summary": "Сочи",
          "value": {
        "title": "Отель Сочи 5 звезд у моря",
        "location": "ул.Моря, 1"
        }
    },
    "2": {
        "summary": "Дубай",
        "value": {
        "title": "Отель Дубай у Бурдж-Халиф",
        "location": "ул.Шейха, 3"
        }
    }
})
):
    async with async_session_maker() as session:
        add_hotel_stat = insert(HotelsOrm).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stat)
        await session.commit()
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