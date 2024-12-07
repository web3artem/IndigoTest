from app.movie.schemas import MovieCreateWithEnum, MovieCreate, MovieUpdate


def convert_movie_schema(movie: MovieCreateWithEnum | MovieUpdate) -> MovieCreate:
    """Функция конвертирует pydantic схему с Enum в другую модель со строковым полем country"""
    country = movie.country.value
    movie_dict = movie.model_dump()
    movie_dict["country"] = country
    return MovieCreate(**movie_dict)
