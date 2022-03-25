from services.iauthentication import IAuthentication
from flask import session, flash
from models.user import User
from services.iusers import IUsers
from services.passhash import PassHash
from services.resources import Services

class Authentication(IAuthentication):
    
    logged_user = User

    @Services.get
    def __init__(self, users : IUsers):
        self.users = users
        
    def log_in_successful(self, email, password) -> bool:       
        found : User = self.users.get_user_by_mail(email)
        if found == None:
            flash(f"Email address {email} is not assigned to any registered members")
            flash(f"Please check for spelling errors or "
            "Click on \"HERE\" below the form if you don't have an account", "error")
            return False
        elif not PassHash.check_pass(found.hashed_pass, password):
            flash("Incorrect Password. Please try again", "error")
            return False
        self.log_session(found.id, found.name, found.email)
        Authentication.logged_user = found
        return True

    def sign_up_successful(self, name, email, password) -> bool:
        if self.users.get_user_by_mail(email) != None:
            flash(f"Email {email} is already assigned to another user.")
            flash(f"Please use an unregistered email or if you have an account go to login.", "error")
            return False
        new_user = User(name, email)
        new_user.password = PassHash.generate_pass(password)
        new_user.serialize(self.users.add_user(new_user))
        self.log_session(new_user.id, name, email)
        Authentication.logged_user = new_user
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
        Authentication.logged_user = User
            
    def get_logged_user(self, id = None) -> User:
        if id == None:
            return Authentication.logged_user
        else:
            return self.users.get_user_by_id(id)

    @staticmethod
    def is_any_logged_in() -> bool:
        return  "id" in session

    def is_logged_in(self, id) -> bool:
        return "id" in session and session["id"] == int(id)
