from models.post import Post
from models.user import User
from services.database.sqlalchemy import SqlAlchemy
from services.interfaces.iusers_repo import IUsersRepo
import re

class SqlAlchemyUsers(IUsersRepo):
    def __init__(self):
        self.db = SqlAlchemy.db
        self.users = SqlAlchemy.Users
        self.deleted = SqlAlchemy.Deleted
    
    def add(self, user : User):
        new_usr = self.users(name = user.name, email = user.email, password = user.hashed_pass, date = user.created, role = user.role)
        self.db.session.add(new_usr)
        self.db.session.commit()
        return new_usr.ownerid
    
    def get_by(self, **kwargs) -> User:
        return self.__get_user(**kwargs)

    def __get_user(self, **kwargs):
        displayed = None
        if "mail" in kwargs:
            displayed = self.db.session.query(self.users).filter_by(email = kwargs["mail"]).first()
        else:
            displayed = self.db.session.query(self.users).filter_by(ownerid = kwargs["id"]).first()
        selected = User(displayed.name, displayed.email, date = displayed.date, role = displayed.role)
        selected.id = displayed.ownerid
        selected.password = displayed.password
        return selected

    def remove(self, user_id):
        if "@" not in user_id:
            deleted_rows = self.db.session.query(SqlAlchemy.Posts.content, self.users.email).\
                outerjoin(SqlAlchemy.Posts, SqlAlchemy.Posts.ownerid == self.users.ownerid).\
                filter(self.users.ownerid == user_id).all()
            for row in deleted_rows:
                deleted = self.deleted(content = row[0], email = row[1])
                self.db.session.add(deleted)
            self.db.session.query(self.users).filter_by(ownerid = user_id).delete()
            self.db.session.commit()
        else:
            self.__permanent_delete(user_id)

    def update(self, usr_id, user : User, pwd):
        dict_new = {"name" : user.name,
                    "email" : user.email}
        if user.role != "":
            dict_new.update({"role" : user.role})
        if pwd != "":
            dict_new.update({"password" : pwd})
        self.db.session.query(self.users).filter_by(ownerid = usr_id).update(dict_new)
        self.db.session.commit()
        
    def get_all(self, clause = "" , inactive_needed  = True, not_filtered = False):
        actives = []
        inactives = []
        columns = [self.users.ownerid, self.users.name, self.users.role]
        if not_filtered:
            actives = self.db.session.query(*columns).all()
        elif clause != "":
            clause = re.findall("\('(.*?)'\)", clause)[0]
            clause = clause.split("', '")
            actives = self.db.session.query(*columns).filter(self.users.role.in_(clause)).all()
        if inactive_needed:
            deleted = self.db.session.query(self.deleted.email).distinct().all()
            for user in deleted:
                inactives.append((user[0], user[0]))
        return actives + inactives

    def get_inactive_posts(self, email):
        result = self.db.session.query(self.deleted.deletedid, self.deleted.content).filter_by(email = email).all()
        posts = []
        for record in result:
            posts.append((str(record.deletedid), Post(email, "No title", record.content)))
        return posts

    def has_account(self, user_id) -> bool:
        q = self.db.session.query(self.users).filter_by(ownerid = user_id)
        return self.db.session.query(q.exists()).scalar()

    def __permanent_delete(self, mail):
        self.db.session.query(self.deleted).delete().filter_by(email = mail)
        self.db.session.commit()