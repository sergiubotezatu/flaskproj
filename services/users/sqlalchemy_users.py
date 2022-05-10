from models.user import User
from services.database.sqlalchemy import SqlAlchemy
from services.interfaces.iusers_repo import IUsersRepo

class SqlAlchemyUsers(IUsersRepo):
    def __init__(self):
        self.db = SqlAlchemy.db
        self.users = SqlAlchemy.Users
    
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
            displayed = self.db.session.query(self.users).filter_by(email = kwargs["mail"]).all()
        else:
            displayed = self.db.session.query(self.users).filter_by(ownerid = kwargs["id"]).all()
        if len(displayed) == 0:
            return None
        else:
            displayed = displayed[0]
        selected = User(displayed.name, displayed.email, date = displayed.date, role = displayed.role)
        selected.id = displayed.ownerid
        return selected 
    
    def remove(self, user_id):
        self.db.session.query(self.users).filter_by(ownerid = user_id).delete()
        self.db.session.commit()

    def update(self, usr_id, user : User, pwd):
        dict_new = {"name" : user.name,
                    "email" : user.email}
        if user.role != "":
            dict_new.update({"role" : user.role})
        if pwd != "":
            dict_new.update({"password" : user.password})
        self.db.session.query(self.users).filter_by(ownerid = usr_id).update(dict_new)
        self.db.session.commit()

    def has_account(self, user_id) -> bool:
        return self.get_by(id = user_id) != None