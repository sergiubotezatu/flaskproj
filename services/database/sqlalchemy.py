from flask_sqlalchemy import SQLAlchemy
from models.db_settings import DBSettings
from flask import current_app
from typing import Text
from sqlalchemy import Column, ForeignKey, Integer, String

class SqlAlchemy:
    db = None

    @classmethod
    def configure(cls, settings : DBSettings):
        current_app.config["SQLALCHEMY_DATABASE_URI"] = settings.to_DB_URI()
        current_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        cls.db = SQLAlchemy(current_app)
