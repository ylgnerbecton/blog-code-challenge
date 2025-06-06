from typing import List, Optional

from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Code Challenge"
    BACKEND_CORS_ORIGINS: List = ["*"]
    ROOT_PATH: str = ""
    LOG_LEVEL: str = "DEBUG"
    TIMEZONE: str = "America/Sao_Paulo"
    DEFAULT_PAGE_SIZE: Optional[int] = 10
    USE_FAKE_AUTHORIZATION: Optional[bool] = Field(default=False)
    DB_HOST: str = Field(default="localhost")
    DB_PORT: int = Field(default=3306)
    DB_NAME: str = Field(default="backoffice")
    DB_USER: str = Field(default="user")
    DB_PASSWORD: str = Field(default="password")

    @property
    def database_url(self) -> str:
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = ConfigDict(env_file=".env", extra="ignore")


settings = Settings()
