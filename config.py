import os

class Config:
    SECRET_KEY = 'sua-chave-secreta'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///knowledge_base.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False 