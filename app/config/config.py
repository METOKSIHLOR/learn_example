from dataclasses import dataclass
from environs import Env

@dataclass
class Postgres:
    user: str
    password: str
    host: str
    port: int
    db: str
    url: str
    sync_url: str

@dataclass
class Config:
    postgres: Postgres

def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        postgres=Postgres(
            user=env("POSTGRES_USER"),
            password=env("POSTGRES_PASSWORD"),
            host=env("POSTGRES_HOST"),
            port=env.int("POSTGRES_PORT"),
            db=env("POSTGRES_DB"),
            url=env("POSTGRES_URL"),
            sync_url=env("POSTGRES_SYNC_URL"),
        )
    )

config = load_config()
