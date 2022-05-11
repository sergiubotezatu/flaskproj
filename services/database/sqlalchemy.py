from flask_sqlalchemy import SQLAlchemy
from models.db_settings import DBSettings
from flask import current_app
from typing import Text
from sqlalchemy.ext.automap import automap_base

class SqlAlchemy:
    db  : SQLAlchemy = None
    Users = None
    Posts = None
    Deleted = None

    @classmethod
    def configure(cls, settings : DBSettings):
        current_app.config["SQLALCHEMY_DATABASE_URI"] = settings.to_DB_URI()
        current_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        cls.db = SQLAlchemy(current_app)
        db = cls.db
        Base = automap_base()
        Base.prepare(db.engine, reflect = True)
        cls.Users = Base.classes.blog_users
        cls.Posts = Base.classes.blog_posts
        cls.Deleted = Base.classes.deleted_users