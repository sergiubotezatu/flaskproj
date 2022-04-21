from services.interfaces.iauthentication import IAuthentication
from flask import redirect, session, flash, url_for
from models.user import User
from services.interfaces.iusers_repo import IUsersRepo
from services.interfaces.Ipassword_hash import IPassHash
from services.dependency_inject.injector import Services
from models.logged_user import Logged_user
from services.auth.session_manager import SessionMngr

class Authentication(SessionMngr, IAuthentication):    
    @Services.get
    def __init__(self, users : IUsersRepo, hasher : IPassHash):
        self.users = users
        self.hasher = hasher
        
    def log_in(self, email, password) -> bool:
        found : User = self.users.get_by(mail = email)
        if found == None or not self.hasher.check_pass(found.hashed_pass, password):
            flash("Incorrect Password or Email. Please try again", "error")
            flash(f"Please check for spelling errors or "
            "Click on \"HERE\" below the form if you don't have an account", "error")
            return redirect(url_for(".log_in"))
        
        self.log_session(found.id, found.name, found.email)
        flash(f"Welcome back, {found.name}!")
        return redirect(url_for("profile.user_profile", user_id = found.id))

    def is_logged_in(self, id) -> bool:
        return "id" in session and session["id"] == int(id)

    def get_logged_user(self) -> Logged_user:
        if "id" in session:
            return Logged_user(session["id"], session["username"], session["email"], session["role"])
        return None

    def edit_logged(self, username, email):
        super().edit_logged(username, email)

    def log_session(self, id, username, email):
        super().log_session(id, username, email)

    def log_out(self):
        super().log_out()
