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
        self.profile = self.register("/view/<user_id>", self.user_profile)
        self.login = self.register("/login", self.log_in)
        self.signup = self.register("/signup", self.sign_up)
        self.edit = self.register("/edit/<user_name>", self.edit_user)
        self.members = self.register("/view/community", self.get_all_users)
        
    def register(self, link, func):
        return self.bp.route(link, methods = ["Get", "Post"])(func)


    def goto_db_setup(self):
        if not DataBase.config.is_configured:
            return redirect(url_for("db_setup.set_database"))

    def user_profile(self, user_id):
        user_id = int(user_id)
        if Session.has_user(user_id):
            logged = self.users.get_user_by_id(user_id)
            return render_template("user.html", user= logged.name, email = logged.email, date = logged.created)
        else:
            return redirect(url_for(".log_in"))

    def log_in(self):
        if request.method == "GET":
            return render_template("login.html")
        else:
            email = request.form.get("mail")
            password = request.form.get("pwd")
            found = self.users.get_user_by_mail(email)
            if found == None:
                flash(f"Email address {email} is not assigned to any registered members")
                flash(f"Please check for spelling errors or "
                "Click on \"HERE\" below the form if you don't have an account", "error")
                return redirect(url_for(".log_in"))
            elif not found.check_pass(password):
                flash("Incorrect Password. Please try again", "error")
                return redirect(url_for(".log_in"))

        Session.add_user(found.id, found.email, found.name)
        return redirect(f"/view/{found.id}")

    def sign_up(self):
        session.clear()
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("pwd")
            if self.__is_existing_user(email):
                flash(f"Email {email} is already assigned to another user. ")
                flash(f"Please use an unregistered email or go to login page", "error")
                return redirect(url_for(".sign_up"))
            else:
                username = request.form.get("username")
                new_user = User(username, email, password)
                self.users.add_user(new_user)
                Session.add_user(new_user.id, email, username)
                flash(f"Welcome, {username}!")
                flash("This is your profile page. Here you can see all of your posts.")
                flash("Click on [Create Post] button to add a new post", "info")
                return redirect(f"view/{new_user.id}")
        return render_template("signup.html")

    def edit_user(self, user_name):
        return render_template("edit_user.html", username = user_name, email = "adf")

    def get_all_users(self):
        return render_template("members.html", allmembers = self.users.get_all())

    def __is_existing_user(self, mail):
        return self.users.get_user_by_mail(mail) != None

class Session:
    @staticmethod
    def has_user(user_id):
        return "id" in session and session["id"] == int(user_id)

    @staticmethod
    def add_user(id, email, username):
        session["id"] = id
        session["logged_in"] = email
        session["username"] = username 
        session.permanent = True

    @staticmethod
    def is_active():
        return "logged_in" in session