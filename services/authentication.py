from services.iauthentication import IAuthentication
from flask import session, flash
from models.user import User
from services.iusers_repo import IUsersRepo
from services.Ipassword_hash import IPassHash
from services.resources import Services
from models.logged_user import Logged_user

class Authentication(IAuthentication):    
    @Services.get
    def __init__(self, users : IUsersRepo, hasher : IPassHash):
        self.users = users
        self.hasher = hasher
        
    def log_in_successful(self, email, password) -> bool:       
        found : User = self.users.get_user_by(mail = email)
        if found == None or not self.hasher.check_pass(found.hashed_pass, password):
            flash("Incorrect Password or Email. Please try again", "error")
            flash(f"Please check for spelling errors or "
            "Click on \"HERE\" below the form if you don't have an account", "error")
            return False
        
        Authentication.log_session(found.id, found.name, found.email)
        return True

    def get_logged_user(self) -> Logged_user:
        if "id" in session:
            return Logged_user(session["id"], session["username"], session["email"])
        return None

    def is_logged_in(self, id) -> bool:
        return "id" in session and session["id"] == int(id)

    @staticmethod
    def log_session(id, username, email):
        session["id"] = id
        session["username"] = username
        session["email"] = email
        session.permanent = True

    @staticmethod
    def log_out():
        session.pop("id")
        session.pop("username")
        session.pop("email")
