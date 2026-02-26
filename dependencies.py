from typing import Annotated
from fastapi import Depends, Query
from pydantic import BaseModel

class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, description="Страница", ge=1)]
    per_page : Annotated[int | None, Query(10, ge=1, lt=30, description="Количество отелей на странице")]

PaginationDep = Annotated[PaginationParams, Depends()]