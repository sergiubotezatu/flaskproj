from flask import Blueprint, render_template, url_for, redirect, request, session, flash
from services.iusersrepo import IUsersRepo
from services.resources import Services
from services.database import DataBase
from models.user import User
from services.passhash import PassHash
from services.authorization import Authorization

class UserProfile:
    @Services.get
    def __init__(self, repo : IUsersRepo):
        self.users = repo
        self.bp = Blueprint("profile", __name__)
        self.to_db_setup = self.bp.before_request(self.goto_db_setup)
        self.profile = self.register("/view/<user_id>", self.user_profile)
        self.edit = self.register("/edit/<user_id>", self.edit_user)
        self.members = self.register("/view/community", self.get_all_users)
        self.admin_choice = self.bp.route("/view/admin_choice")(self.chose_users_list)
        self.removed_users = self.bp.route("/view/inactive")(self.get_all_inactive)
        self.removed_user = self.register("/view/old_users/<email>", self.inactive_user)

    def register(self, link, func):
        return self.bp.route(link, methods = ["Get", "Post"])(func)

    def goto_db_setup(self):
        if not DataBase.config.is_configured:
            return redirect(url_for("db_setup.set_database"))

    def user_profile(self, user_id):
        user_id = int(user_id)
        if request.method == "POST":
            return self.check_for_logout()
        
        logged = self.users.get_user_by_id(user_id)
        owned_posts = self.users.get_posts(user_id)
        return render_template("user.html",
        user_id = logged.id,
        user= logged.name,
        email = logged.email,
        date = logged.created,
        modified = logged.modified,
        posts = owned_posts)
 
    @Authorization.owner_or_admin
    def edit_user(self, user_id):
        user_id = int(user_id)
        editable : User = self.users.get_user_by_id(user_id)
        if request.method == "POST":
            if PassHash.check_pass(editable.hashed_pass, request.form.get("oldpass")):
                self.__update_info(user_id)
                return redirect(url_for(".user_profile", user_id = user_id))
            else:
                flash(f"Old password does not match current one. Please try again", "error")
                
        return render_template("edit_user.html", username = editable.name, email = editable.email)

    def get_all_users(self):
        return render_template("members.html", prefix = "view", allmembers = self.users.get_all())

    @Authorization.admin_required
    def chose_users_list(self):
        return render_template("admin_choice.html")

    def get_all_inactive(self):
        return render_template("members.html", prefix = "view/archive", allmembers = self.users.get_all_inactive())

    @Authorization.admin_required
    def inactive_user(self, email):
        if request.method == "POST":
            return self.check_for_logout()
        removed_posts = self.users.get_inactive_posts(email)
        return render_template("user.html", 
        user_id = email,
        user= "Deleted User",
        email = email,
        date = "N/A",
        modified = None,
        posts = removed_posts)        

    def __update_info(self, user_id):
        new_name = request.form.get("username")
        new_mail = request.form.get("email", user_id)
        new_password = self.__hash_if_new_pass(request.form.get("pwd"))
        session["name"] = new_name
        session["email"] = new_mail
        self.users.update_user(user_id, User(new_name, new_mail), new_password)

    def check_for_log_out(self):
        if request.form.get("action") == "logout":
            flash(f"You have been logged out. See you again soon!")
        else:
            to_delete = self.users.get_user_by_id(session["id"])
            flash(f"Your membership has been canceled.")
            self.users.remove_user(to_delete)
        return redirect(url_for("home.front_page"))

    def __hash_if_new_pass(self, input):
        if input != "":
            return PassHash.generate_pass(input)
        return input

