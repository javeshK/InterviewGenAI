import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:

    SECRET_KEY = os.getenv("SECRET_KEY", "interviewgenai_secret_key")

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    GEMINI_MODEL = "gemini-3.5-flash"

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" +
        os.path.join(BASE_DIR, "interview.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False