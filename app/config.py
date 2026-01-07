from pydantic import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    mongodb_uri: str
    mongodb_db_name: str

    class Config:
        env_file = ".env"

settings = Settings()