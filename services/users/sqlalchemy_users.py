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
        self.orm = orm
        
    def add(self, user : User):
        new_usr = self.orm.Users(name = user.name, email = user.email, password = user.hashed_pass, date = user.created, role = user.role)
        self.orm.session.add(new_usr)
        self.orm.session.commit()
        return new_usr.ownerid
    
    def get_by(self, **kwargs) -> User:
        return self.__get_user(**kwargs)

    def __get_user(self, **kwargs):
        displayed = None
        if "mail" in kwargs:
            displayed = self.orm.session.query(self.orm.Users).filter_by(email = kwargs["mail"]).first()
        else:
            displayed = self.orm.session.query(self.orm.Users).filter_by(ownerid = kwargs["id"]).first()
        selected = User(displayed.name, displayed.email, date = displayed.date, role = displayed.role)
        selected.id = displayed.ownerid
        selected.password = displayed.password
        return selected

    def remove(self, user_id):
        if "@" not in user_id:
            deleted_rows = self.orm.session.query(SqlAlchemy.Posts.content, self.orm.Users.email).\
                outerjoin(SqlAlchemy.Posts, SqlAlchemy.Posts.ownerid == self.orm.Users.ownerid).\
                filter(self.orm.Users.ownerid == user_id).all()
            for row in deleted_rows:
                deleted = self.orm.Deleted(content = row[0], email = row[1])
                self.orm.session.add(deleted)
            self.orm.session.query(self.orm.Users).filter_by(ownerid = user_id).delete()
            self.orm.session.commit()
        else:
            self.__permanent_delete(user_id)

    def update(self, usr_id, user : User, pwd):
        dict_new = {"name" : user.name,
                    "email" : user.email}
        if user.role != "":
            dict_new.update({"role" : user.role})
        if pwd != "":
            dict_new.update({"password" : pwd})
        self.orm.session.query(self.orm.Users).filter_by(ownerid = usr_id).update(dict_new)
        self.orm.session.commit()
        
    def get_all(self, clause = "" , inactive_needed  = True, not_filtered = False):
        actives = []
        inactives = []
        columns = [self.orm.Users.ownerid, self.orm.Users.name, self.orm.Users.role]
        if not_filtered:
            actives = self.orm.session.query(*columns).all()
        elif clause != "":
            clause = re.findall("\('(.*?)'\)", clause)[0]
            clause = clause.split("', '")
            actives = self.orm.session.query(*columns).filter(self.orm.Users.role.in_(clause)).all()
        if inactive_needed:
            deleted = self.orm.session.query(self.orm.Deleted.email).distinct().all()
            for user in deleted:
                inactives.append((user[0], user[0]))
        return actives + inactives

    def get_inactive_posts(self, email):
        result = self.orm.session.query(self.orm.Deleted.deletedid, func.substr(self.orm.Deleted.content, 0, 150)).filter_by(email = email).all()
        posts = []
        for record in result:
            posts.append((str(record.deletedid), Post(email, "No title", record[1])))
        return posts

    def has_account(self, mail) -> bool:
        q = self.orm.session.query(self.orm.Users).filter_by(email = mail)
        return self.orm.session.query(q.exists()).scalar()

    def __permanent_delete(self, mail):
        self.orm.session.query(self.orm.Deleted).filter_by(email = mail).delete()
        self.orm.session.commit()