import os


class Config:
    DATABASE = "/tmp/dubaitoursteam.db"
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY") or "very_long_and_secret_key"