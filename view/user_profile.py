from flask import Blueprint, render_template, url_for, redirect, request, session, flash
from services.interfaces.iauthorization import IAuthorization
from services.users.authentication import Authentication
from services.interfaces.iusers_repo import IUsersRepo
from services.dependency_inject.injector import Services
from models.user import User
from services.interfaces.Ipassword_hash import IPassHash
from services.users.access_decorators import AccessDecorators, decorator

class UserProfile:
    authorizator = AccessDecorators(IAuthorization)

    @Services.get
    def __init__(self, repo : IUsersRepo, hasher : IPassHash):
        self.users = repo
        self.hasher = hasher
        self.bp = Blueprint("profile", __name__)
        self.to_db_setup = self.bp.before_request(self.goto_db_setup)
        self.profile = self.register("/view/<user_id>", self.user_profile)
        self.edit = self.register("/edit/<user_id>", self.edit_user)
        self.members = self.register("/view/community", self.get_all_users)
        self.signup = self.register("/signup", self.sign_up)
        self.admin_choice = self.bp.route("/view/admin_choice")(self.chose_users_list)
        self.removed_users = self.bp.route("/view/inactive")(self.get_all_inactive)
        self.removed_user = self.register("/view/old_users/<email>", self.inactive_user)
       
    def register(self, link, func):
        return self.bp.route(link, methods = ["Get", "Post"])(func)

    @decorator.only_once
    def goto_db_setup(self):
        return redirect(url_for("db_setup.set_database"))

    def sign_up(self):
        if request.method == "POST":
            email = request.form.get("email")
            pwd = request.form.get("pwd")
            username = request.form.get("username")
            if not self.__sign_up_validated(username, email):
                return redirect(url_for(".sign_up"))
            else:
                print("YYY")
                new_user = User(username, email)
                new_user.password = self.hasher.generate_pass(pwd)
                new_user.id = self.users.add_user(new_user)
                Authentication.log_session(new_user.id, username, email)
                return redirect(url_for("profile.user_profile", user_id = new_user.id))
        return render_template("signup.html")

    def user_profile(self, user_id):
        user_id = int(user_id)
        if request.method == "POST":
            return self.check_for_log_out()
        
        logged = self.users.get_user_by(id = user_id)
        owned_posts = self.users.get_posts(user_id)
        return render_template("user.html",
        user_id = logged.id,
        user= logged.name,
        email = logged.email,
        date = logged.created,
        modified = logged.modified,
        posts = owned_posts)
 
    @authorizator.owner_or_admin
    def edit_user(self, user_id):
        user_id = int(user_id)
        editable : User = self.users.get_user_by(id = user_id)
        if request.method == "POST":
            if self.hasher.check_pass(editable.hashed_pass, request.form.get("oldpass")):
                self.__update_info(user_id)
                return redirect(url_for(".user_profile", user_id = user_id))
            else:
                flash(f"Old password does not match current one. Please try again", "error")
                
        return render_template("edit_user.html", username = editable.name, email = editable.email)

    def get_all_users(self):
        return render_template("members.html", prefix = "view", allmembers = self.users.get_all())

    @authorizator.admin_required
    def chose_users_list(self):
        return render_template("admin_choice.html")

    def get_all_inactive(self):
        return render_template("members.html", prefix = "view/archive", allmembers = self.users.get_all_inactive())

    @authorizator.admin_required
    def inactive_user(self, email):
        if request.method == "POST":
            return self.check_for_log_out()
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
            to_delete = self.users.get_user_by(id = session["id"])
            Authentication.log_out()
            flash(f"Your membership has been canceled.")
            self.users.remove_user(to_delete)
        return redirect(url_for("home.front_page"))

    def __hash_if_new_pass(self, input):
        if input != "":
            return self.hasher.generate_pass(input)
        return input

    def __sign_up_validated(self, name, email):
        if self.users.get_user_by(mail = email) != None:
            flash(f"Email {email} is already assigned to another user.")
            flash(f"Please use an unregistered email or if you have an account go to login.", "error")
            return False
        flash(f"Welcome, {name}!")
        flash("This is your profile page. Here you can see all of your posts.")
        flash("Select Create new post to add a new post", "info")
        return True


