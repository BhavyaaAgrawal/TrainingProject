import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str

    def __init__(self) -> None:
        database_url = os.getenv("DATABASE_URL")
        if database_url is None:
            raise RuntimeError("DATABASE_URL environment variable is not set")
        self.DATABASE_URL = database_url

settings = Settings()
