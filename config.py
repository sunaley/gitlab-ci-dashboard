from functools import lru_cache
from pydantic import BaseSettings


@lru_cache()
def get_settings():
    return Settings()


class Settings(BaseSettings):
    GITLAB_API_TOKEN: str
    GITLAB_API_URL: str = 'https://gitlab.com/api/v4/'
    GITLAB_GROUP: str

    class Config:
        env_file = ".env"
