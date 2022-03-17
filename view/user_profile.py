from flask import Blueprint, render_template, url_for, redirect, request, session, flash
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
        self.edit = self.register("/edit/<user_id>", self.edit_user)
        self.members = self.register("/view/community", self.get_all_users)
        
    def register(self, link, func):
        return self.bp.route(link, methods = ["Get", "Post"])(func)


    def goto_db_setup(self):
        if not DataBase.config.is_configured:
            return redirect(url_for("db_setup.set_database"))

    def user_profile(self, user_id):
        user_id = int(user_id)
        if request.method == "POST":
            Session.empty()
            if request.form.get("action") == "logout":
                flash(f"You have logged out. See you again soon!")
            else:
                to_delete = self.users.get_user_by_id(user_id)
                flash(f"Your membership has been canceled.")
                self.users.remove_user(to_delete)
            return redirect(url_for("home.front_page"))
        
        logged = self.users.get_user_by_id(user_id)
        return render_template("user.html",
        user_id = logged.id,
        user= logged.name,
        email = logged.email,
        date = logged.created,
        modified = logged.modified)

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
        flash(f"Welcome back, {found.name}!")
        Session.add_user(found.id, found.email, found.name)
        return redirect(f"/view/{found.id}")

    def sign_up(self):
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("pwd")
            if self.__is_existing_user(email):
                flash(f"Email {email} is already assigned to another user.")
                flash(f"Please use an unregistered email or if you have an account go to login.", "error")
                return redirect(url_for(".sign_up"))
            else:
                username = request.form.get("username")
                new_user = User(username, email, password)
                self.users.add_user(new_user)
                Session.add_user(new_user.id, email, username)
                flash(f"Welcome, {username}!")
                flash("This is your profile page. Here you can see all of your posts.")
                flash("Select Create new post to add a new post", "info")
                return redirect(f"view/{new_user.id}")
        return render_template("signup.html")

    def edit_user(self, user_id):
        user_id = int(user_id)
        editable = self.users.get_user_by_id(user_id)
        if request.method == "POST":
            if editable.check_pass(request.form.get("oldpass")):
                new_name = request.form.get("username")
                new_mail = request.form.get("email", user_id)
                new_password = request.form.get("pwd")
                Session.modify_user(user_id, new_mail, new_name)
                self.users.update_user(user_id, User(new_name, new_mail, new_password), new_password)
                return redirect(url_for(".user_profile", user_id = user_id))
            else:
                flash(f"Old password does not match current one. Please try again", "error")
                
        return render_template("edit_user.html", username = editable.name, email = editable.email)

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
    def modify_user(id, email, username):
        Session.empty()
        Session.add_user(id, email, username)
        
    @staticmethod
    def is_active():
        return "logged_in" in session

    @staticmethod
    def empty():
        session.pop("id")
        session.pop("logged_in")
        session.pop("username")