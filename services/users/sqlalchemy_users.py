from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from models.post import Post
from models.user import User
from services.database.sqlalchemy import SqlAlchemy
from services.dependency_inject.injector import Services
from services.interfaces.idata_base import IDataBase
from services.interfaces.iusers_repo import IUsersRepo
import re

class SqlAlchemyUsers(IUsersRepo):
    @Services.get
    def __init__(self, orm : IDataBase):
        self.session = orm.session
        self.users = orm.Users
        self.deleted = orm.Deleted
    
    def add(self, user : User):
        new_usr = self.users(name = user.name, email = user.email, password = user.hashed_pass, date = user.created, role = user.role)
        self.session.add(new_usr)
        self.session.commit()
        return new_usr.ownerid
    
    def get_by(self, **kwargs) -> User:
        return self.__get_user(**kwargs)

    def __get_user(self, **kwargs):
        displayed = None
        if "mail" in kwargs:
            displayed = self.session.query(self.users).filter_by(email = kwargs["mail"]).first()
        else:
            displayed = self.session.query(self.users).filter_by(ownerid = kwargs["id"]).first()
        selected = User(displayed.name, displayed.email, date = displayed.date, role = displayed.role)
        selected.id = displayed.ownerid
        selected.password = displayed.password
        return selected

    def remove(self, user_id):
        if "@" not in user_id:
            deleted_rows = self.session.query(SqlAlchemy.Posts.content, self.users.email).\
                outerjoin(SqlAlchemy.Posts, SqlAlchemy.Posts.ownerid == self.users.ownerid).\
                filter(self.users.ownerid == user_id).all()
            for row in deleted_rows:
                deleted = self.deleted(content = row[0], email = row[1])
                self.session.add(deleted)
            self.session.query(self.users).filter_by(ownerid = user_id).delete()
            self.session.commit()
        else:
            self.__permanent_delete(user_id)

    def update(self, usr_id, user : User, pwd):
        dict_new = {"name" : user.name,
                    "email" : user.email}
        if user.role != "":
            dict_new.update({"role" : user.role})
        if pwd != "":
            dict_new.update({"password" : pwd})
        self.session.query(self.users).filter_by(ownerid = usr_id).update(dict_new)
        self.session.commit()
        
    def get_all(self, clause = "" , inactive_needed  = True, not_filtered = False):
        actives = []
        inactives = []
        columns = [self.users.ownerid, self.users.name, self.users.role]
        if not_filtered:
            actives = self.session.query(*columns).all()
        elif clause != "":
            clause = re.findall("\('(.*?)'\)", clause)[0]
            clause = clause.split("', '")
            actives = self.session.query(*columns).filter(self.users.role.in_(clause)).all()
        if inactive_needed:
            deleted = self.session.query(self.deleted.email).distinct().all()
            for user in deleted:
                inactives.append((user[0], user[0]))
        return actives + inactives

    def get_inactive_posts(self, email):
        result = self.session.query(self.deleted.deletedid, func.substr(self.deleted.content, 0, 150)).filter_by(email = email).all()
        posts = []
        for record in result:
            posts.append((str(record.deletedid), Post(email, "No title", record[1])))
        return posts

    def has_account(self, mail) -> bool:
        q = self.session.query(self.users).filter_by(email = mail)
        return self.session.query(q.exists()).scalar()

    def __permanent_delete(self, mail):
        self.session.query(self.deleted).filter_by(email = mail).delete()
        self.session.commit()