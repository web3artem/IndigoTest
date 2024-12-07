from pydantic import BaseModel, ConfigDict


class FavoriteMovieResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    country: str
    director: str
    release_year: int
