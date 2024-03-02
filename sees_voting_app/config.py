import os
from dotenv import load_dotenv
from pathlib import Path

# Find the .env file in the parent directory
env_path = Path(__file__).resolve().parents[2] / ".env"

# Load the environment variables from the .env file
load_dotenv(env_path)


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")
