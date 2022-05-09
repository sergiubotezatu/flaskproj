from email.policy import default
from typing import Text
from sqlalchemy import Column, ForeignKey, Integer, String
from services.database.sqlalchemy import SqlAlchemy

db = SqlAlchemy.db

class Users(SqlAlchemy.db.Model):
    ownerID = Column(Integer, primary_key=True)
    name = Column(String(30))
    email = Column(String(200), unique=True)
    password = Column(String)
    date = Column(String(50))
    date_modified = Column(String(50))
    role = Column(String(20), default="regular")

class Posts(db.Model):
    PostID = Column(Integer, primary_key=True)
    OwnerID = Column(Integer, ForeignKey("User.ownerID", ondelete="all, delete"))
    Title = Column(String(200))
    Content = Column(Text(5000))
    date = Column(String(50))
    date_modified = Column(String(50))