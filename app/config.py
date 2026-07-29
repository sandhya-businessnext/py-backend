from urllib.parse import quote_plus

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST:str
    POSTGRES_PORT:int
    POSTGRES_DB:str
    model_config = SettingsConfigDict(env_file="./.env",
                                      ignore_empty=True, # ignores empty values, optional settings
                                      extra="ignore") # ignores fields not in class
    @computed_field
    @property
    def POSTGRES_URL(self) -> str:
         return (
            f"postgresql+asyncpg://{self.POSTGRES_USERNAME}:{quote_plus(self.POSTGRES_PASSWORD)}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
      

db_settings = DatabaseSettings()


class SecuritySettings(BaseSettings):
    JWT_ALGORITHM: str
    JWT_SECRET_KEY: str

    model_config = SettingsConfigDict(env_file="./.env", ignore_empty=True, # ignores empty values, optional settings
                                      extra="ignore") # ignores fields not in class

security_settings = SecuritySettings()

