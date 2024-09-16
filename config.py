import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    EDAMAM_API_KEY = os.getenv('EDAMAM_API_KEY')
    EDAMAM_APP_ID= os.getenv('EDAMAM_APP_ID')
    SPOONACULAR_API_KEY = os.getenv('SPOONACULAR_API_KEY')
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    GOOGLE_DISCOVERY_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    WTF_CSRF_ENABLED = True


class DevelopmentConfig(Config):
    DEBUG = True # enables debug mode in flask
    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI', 'sqlite:///:memory:') # uses in memory database for testing


class ProductionConfig(Config):
    DEBUG = False