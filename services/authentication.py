from services.iauthentication import IAuthentication
from flask import session, flash, request
from models.user import User
from services.iusers import IUsers
from services.passhash import PassHash

class Authentication(IAuthentication):
    logged_user = User

    def __init__(self, users : IUsers):
        self.users = users
        
    def log_in_succesful(self, email, password) -> bool:       
        found : User = self.users.get_user_by_mail(email)
        if found == None:
            flash(f"Email address {email} is not assigned to any registered members")
            flash(f"Please check for spelling errors or "
            "Click on \"HERE\" below the form if you don't have an account", "error")
            return False
        elif not PassHash.check_pass(found.hashed_pass, password):
            flash("Incorrect Password. Please try again", "error")
            return False
        Session.log_session(found.id, found.name, found.email)
        Authentication.logged_user = found
        return True

    def sign_up_succesful(self, name, email, password) -> int:
        if self.users.get_user_by_mail(email) != None:
            flash(f"Email {email} is already assigned to another user.")
            flash(f"Please use an unregistered email or if you have an account go to login.", "error")
            return -1
        new_user = User(name, email)
        new_user.set_pass(password, True)
        new_user.serialize(self.users.add_user(new_user))
        Session.log_session(new_user.id, name, email)
        flash(f"Welcome, {name}!")
        flash("This is your profile page. Here you can see all of your posts.")
        flash("Select Create new post to add a new post", "info")
        return new_user.id

    def log_out(self):
        Session.log_out()

    def is_any_logged_in(self) -> bool:
        return Session.is_active()

    def is_logged_in(self, id) -> bool:
        return Session.has_user(id)

    def get_logged_user(self) -> User:
        return Authentication.logged_user

class Session:
    @staticmethod
    def has_user(user_id):
        return "id" in session and session["id"] == int(user_id)

    @staticmethod
    def log_session(id, name, mail):
        session["id"] = id
        session["name"] = name
        session["email"] = mail
        session.permanent = True

    @staticmethod
    def is_active():
        return "id" in session

    @staticmethod
    def log_out():
        session.pop("id")
        session.pop("logged_in")
        session.pop("username")