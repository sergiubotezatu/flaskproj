from services.iauthentication import IAuthentication
from models.user import User
from flask import Blueprint, request, redirect, render_template, url_for, flash
from services.resources import Services
from services.database import DataBase

class UserAuthenticate:
    @Services.get
    def __init__(self, authenticator : IAuthentication):
        self.authenticator = authenticator
        self.bp = Blueprint("authentication", __name__)
        self.to_db_setup = self.bp.before_request(self.goto_db_setup)
        self.login = self.register("/login", self.log_in)
        self.signup = self.register("/signup", self.sign_up)
        self.logout = self.bp.route("/logout")(self.log_out)

    def goto_db_setup(self):
        if not DataBase.config.is_configured:
            return redirect(url_for("db_setup.set_database"))

    def register(self, link, func):
        return self.bp.route(link, methods = ["Get", "Post"])(func)

    def log_in(self):
        if request.method == "GET":
            return render_template("login.html")
        else:
            email = request.form.get("mail")
            password = request.form.get("pwd")
            if not self.authenticator.log_in_successful(email, password):
                return redirect(url_for(".log_in"))

        found = self.authenticator.get_logged_user()
        flash(f"Welcome back, {found.name}!")
        return redirect(url_for("profile.user_profile", user_id = found.id))

    def sign_up(self):
        if request.method == "POST":
            email = request.form.get("email")
            pwd = request.form.get("pwd")
            username = request.form.get("username")
            if not self.authenticator.sign_up_successful(username, email, pwd):
                return redirect(url_for(".sign_up"))
            else:
                signed_id = self.authenticator.get_logged_user().id              
                return redirect(url_for("profile.user_profile", user_id = signed_id))
        return render_template("signup.html")

    def log_out(self):
        self.authenticator.log_out()
        flash(f"You have been logged out. See you again soon!")
        return redirect(url_for("home.front_page"))