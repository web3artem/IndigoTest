from fastapi import FastAPI
from app.user.routes import router as user_router
from app.movie.routes import router as movie_router
from app.favorite.routes import router as favorite_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Indigo VC CRUD",
        docs_url="/api/docs",
        debug=True,
    )
    app.include_router(user_router, prefix="/api/user")
    app.include_router(movie_router, prefix="/api/movie")
    app.include_router(favorite_router, prefix="/api")
    return app
