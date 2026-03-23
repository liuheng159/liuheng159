from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = "Backend Skills Starter"
    version: str = "0.1.0"
    environment: str = "development"
    host: str = "127.0.0.1"
    port: int = 8000


settings = Settings()
