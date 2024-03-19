from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = False
    environment: str
    database_url: str
    pod_management_service_url: str

    class Config:
        env_file = ".env"


settings = Settings()
