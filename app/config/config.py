from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    POSTGRES_PASSWORD: str
    MODE: str

    @property
    def ASYNC_DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def test_postgres_db(self) -> str:
        return f"test_{self.DB_NAME}"

    @property
    def test_postgres_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.test_postgres_db}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
