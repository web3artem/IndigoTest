from pydantic import BaseModel, Field


class UserBaseModel(BaseModel):
    first_name: str = Field(max_length=50)
    second_name: str = Field(max_length=50)
    nickname: str = Field(max_length=50)


class UserCreate(UserBaseModel):
    ...


class UserUpdate(UserBaseModel):
    ...
