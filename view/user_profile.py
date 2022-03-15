from flask import Blueprint, render_template, current_app, url_for, redirect, request, session, flash
from services.iusers import IUsers
from services.resources import Services
from services.database import DataBase
from models.user import User

class UserProfile:
    @Services.get
    def __init__(self, repo : IUsers):
        self.users = repo
        self.bp = Blueprint("profile", __name__)
        self.to_db_setup = self.bp.before_request(self.goto_db_setup)
        self.profile = self.register("/view/<name>", self.user_profile)
        self.login = self.register("/login", self.log_in)
        self.signup = self.register("/signup", self.sign_up)
        
    def register(self, link, func):
        return self.bp.route(link, methods = ["Get", "Post"])(func)

    def goto_db_setup(self):
        if not DataBase.config.is_configured:
            return redirect(url_for("db_setup.set_database"))

    def user_profile(self, user_name):
        print(user_name)
        if "profile" in session and session["profile"] == user_name:
            return render_template("user.html", user= user_name)
        else:
            return redirect(url_for(".log_in"))

    def log_in(self):
        if request.method == "GET":
            return render_template("login.html")
        else:
            username = request.form.get("username")
            password = request.form.get("pwd")
            found = self.users.get_user_by_name(username)
            if found == None:
                flash(f"Username {username} is not assigned to any registered members\nCheck for spelling errors"
                "Click on \"Here\" below the form if you don't have an account", "error")
                return redirect(url_for(".log_in"))
            elif not found.check_pass(password):
                flash("Incorrect Password. Please try again", "error")
                return redirect(url_for(".log_in"))

        session.permanent = True
        session["profile"] = username
        return redirect(f"/view/{username}")

    def sign_up(self):
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("pwd")
            if self.__is_existing_user(username):
                flash(f"Username {username} is already assigned to another user. "
               "Please use a different userName", "error")
                return redirect(url_for(".sign_up"))
            else:
                email = request.form.get("email")
                self.users.add_user(User(username, email, password))
                session["profile"] = username
                flash(f"Welcome, {username}!\nThis is your profile page. Here you can see all of your posts "
                "Click on [Create Post] button to add a new post", "info")
                return redirect(f"/view/{username}")
        return render_template("signup.html")

    def __is_existing_user(self, username):
        return self.users.get_user_by_name(username) != None
