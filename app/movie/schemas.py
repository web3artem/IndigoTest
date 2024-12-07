from pydantic import BaseModel, Field
from .enums import CountryEnum


class MovieBaseModel(BaseModel):
    title: str
    release_year: int = Field(gt=1800, le=9999)
    director: str = Field(max_length=100)


class MovieCreateWithEnum(MovieBaseModel):
    country: CountryEnum


class MovieCreate(MovieBaseModel):
    country: str


class MovieUpdate(MovieBaseModel):
    country: str


class MovieUpdateWithEnum(MovieBaseModel):
    country: CountryEnum
