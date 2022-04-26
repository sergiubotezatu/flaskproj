from flask import session
from models.logged_user import Logged_user
from services.dependency_inject.injector import Services
from services.interfaces.isession_mngr import ISessionMNGR

class SessionMngr(ISessionMNGR):

    def edit_logged(self, username, email):
        session["username"] = username
        session["email"] = email
        
    def log_session(self, id, username, email, role):
        session["id"] = id
        session["username"] = username
        session["email"] = email
        session["role"] = role
        session.permanent = True    

    def log_out(self):
        session.pop("id")
        session.pop("username")
        session.pop("email")
        session.pop("role")

    def get_logged_user(self) -> Logged_user:
        if "id" in session:
            return Logged_user(session["id"], session["username"], session["email"], session["role"])
        return None

        