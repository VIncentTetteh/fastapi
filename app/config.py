from hashlib import algorithms_available
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_username: str
    database_password: str
    database_port: str
    database_name:str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int = 0

    class Config:
        env_file = ".env" 

settings = Settings()