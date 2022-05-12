from services.interfaces.iauthentication import IAuthentication
from flask import redirect, render_template, session, flash, url_for
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
            flash("Incorrect Password or Email. Please try again.", "error")
            flash(f"Check for spelling errors or "
            "Click on \"HERE\" below the form if you don't have an account", "error")
            return render_template("login.html", mail = email)
        
        self.log_session(found.id, found.name, found.email, found.role)
        flash(f"Welcome back, {found.name}!")
        return redirect(url_for("profile.user_profile", user_id = found.id, pg = ["1"]))

    def is_logged_in(self, id) -> bool:
        return "id" in session and session["id"] == int(id)