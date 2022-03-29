from services.iauthentication import IAuthentication
from flask import session, flash
from models.user import User
from services.iusersrepo import IUsersRepo
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
        
        self.log_session(found.id, found.name, found.email)
        return True

    def sign_up_successful(self, name, email, password) -> bool:
        if self.users.get_user_by(mail = email) != None:
            flash(f"Email {email} is already assigned to another user.")
            flash(f"Please use an unregistered email or if you have an account go to login.", "error")
            return False
        new_user = User(name, email)
        new_user.password = self.hasher.generate_pass(password)
        new_user.id = self.users.add_user(new_user)
        self.log_session(new_user.id, name, email)
        flash(f"Welcome, {name}!")
        flash("This is your profile page. Here you can see all of your posts.")
        flash("Select Create new post to add a new post", "info")
        return True

    def log_session(self, id, username, email):
        session["id"] = id
        session["username"] = username
        session["email"] = email
        session.permanent = True

    def log_out(self):
        session.pop("id")
        session.pop("username")
        session.pop("email")
       
    def get_logged_user(self) -> Logged_user:
        if "id" in session:
            return Logged_user(session["id"], session["username"], session["email"])
        return None

    @staticmethod
    def is_active_session() -> bool:
        return "id" in session

    def is_logged_in(self, id) -> bool:
        return "id" in session and session["id"] == int(id)
