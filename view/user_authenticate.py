from services.database.database import DataBase
from services.interfaces.iauthentication import IAuthentication
from models.user import User
from flask import Blueprint, request, redirect, render_template, url_for, flash
from services.dependency_inject.injector import Services
from services.interfaces.iauthorization import IAuthorization
from services.users.access_decorators import AccessDecorators

class UserAuthenticate:
    authorizator = AccessDecorators(IAuthorization)

    @Services.get
    def __init__(self, authenticator : IAuthentication):
        self.authenticator = authenticator
        self.bp = Blueprint("authentication", __name__)
        self.to_db_setup = self.bp.before_request(self.goto_db_setup)
        self.login = self.register("/login", self.log_in)
        self.logout = self.bp.route("/logout")(self.log_out)
        
    def goto_db_setup(self):
        if not DataBase.config.is_configured:
            return redirect(url_for("db_setup.set_database"))

    def register(self, link, func):
        return self.bp.route(link, methods = ["Get", "Post"])(func)

    @authorizator.logged_not_allowed
    def log_in(self):
        if request.method == "GET":
            return render_template("login.html")
        else:
            email = request.form.get("mail")
            password = request.form.get("pwd")
            return self.authenticator.log_in(email, password)

    def log_out(self):
        self.authenticator.log_out()
        flash(f"You have been logged out. See you again soon!")
        return redirect(url_for("home.front_page"))
