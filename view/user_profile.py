from flask import Blueprint, render_template, url_for, redirect, request, session, flash
from models.logged_user import Logged_user
from services.database.database import DataBase
from services.interfaces.iauthorization import IAuthorization
from services.auth.authentication import Authentication
from services.interfaces.ifilters import IFilters
from services.interfaces.isession_mngr import ISessionMNGR
from services.interfaces.iusers_repo import IUsersRepo
from services.dependency_inject.injector import Services
from models.user import User
from services.interfaces.Ipassword_hash import IPassHash
from services.users.access_decorators import AccessDecorators

class UserProfile:
    authorizator = AccessDecorators(IAuthorization, ISessionMNGR)

    @Services.get
    def __init__(self, repo : IUsersRepo, hasher : IPassHash, active_usr : ISessionMNGR, filter : IFilters):
        self.users = repo
        self.hasher = hasher
        self.active_usr = active_usr
        self.filter = filter
        self.bp = Blueprint("profile", __name__)
        self.to_db_setup = self.bp.before_request(self.goto_db_setup)
        self.profile = self.register("/view/<user_id>/", self.user_profile)
        self.members = self.register("/view/community", self.get_all_users)
        self.signup = self.register("/signup", self.sign_up)
        self.removed_user = self.register("/view/old_users/<email>/", self.inactive_user)
        self.edit = self.register("/edit/<user_id>", self.edit_user)
        self.create_new = self.register("/create", self.create)
        self.activate_old = self.register("/create/<name>/<email>", self.create)
        self.activate_old = self.register("/activate/<user_id>", self.activate)
        self.DISPLAYED_LIMIT = 5
       
    def register(self, link, func):
        return self.bp.route(link, methods = ["Get", "Post"])(func)

    def goto_db_setup(self):
        if not DataBase.config.is_configured:
            return redirect(url_for("db_setup.set_database"))

    @authorizator.logged_not_allowed
    def sign_up(self):
        if request.method == "POST":
            email = request.form.get("email")
            pwd = request.form.get("pwd")
            username = request.form.get("username")
            if not self.__sign_up_validated(username, email):
                return redirect(url_for(".sign_up"))
            else:
                new_user = User(username, email)
                new_user.password = self.hasher.generate_pass(pwd)
                new_user.id = self.users.add(new_user)
                self.active_usr.log_session(new_user.id, username, email, new_user.role)
                return redirect(url_for(".user_profile", user_id = new_user.id, pg = ["1"]))
        return render_template("signup.html")

    @authorizator.member_required
    def user_profile(self, user_id):
        if request.method == "POST":
            self.delete_user()
            return redirect(url_for("home.front_page"))
        displayed = self.users.get_by(id = user_id)
        filter_params = {"user_id" : [user_id], "name" : [displayed.name]}
        page = int(request.args["pg"])
        owned_posts = self.filter.apply(filter_params, page)
        is_editter = self.__is_editter(self.active_usr.get_logged_user(), user_id)
        return render_template("user.html",
                                edit_allowed = is_editter,
                                user_id = displayed.id,
                                name= displayed.name,
                                email = displayed.email,
                                date = displayed.created,
                                modified = displayed.modified,
                                posts = owned_posts[0:self.DISPLAYED_LIMIT],
                                pg = page,
                                next = len(owned_posts) > 0 and owned_posts[-1][2] > self.DISPLAYED_LIMIT)
 
    @authorizator.owner_or_admin
    def edit_user(self, user_id):
        user_id = int(user_id)
        editable : User = self.users.get_by(id = user_id)
        if request.method == "POST":
            identity_checker = request.form.get("oldpass")
            if identity_checker == "" or self.hasher.check_pass(editable.hashed_pass, identity_checker) :
                self.__update_info(user_id)
                return redirect(url_for(".user_profile", user_id = user_id))
            else:
                flash(f"Old password does not match current one. Please try again", "error")
        
        return render_template("edit_user.html",
                                is_admin = self.__is_editter(self.active_usr.get_logged_user()),
                                username = editable.name,
                                email = editable.email,
                                role = editable.role)

    @authorizator.admin_required
    def get_all_users(self):
        return render_template("members.html", allmembers = self.users.get_all())

    @authorizator.admin_required
    def chose_users_list(self):
        return render_template("admin_choice.html")

    @authorizator.admin_required
    def inactive_user(self, email):
        if request.method == "POST":
            self.delete_user()
            return redirect(url_for("home.front_page"))
        removed_posts = self.users.get_inactive_posts(email)
        return render_template("user.html", 
        user_id = email,
        user= "Deleted User",
        email = email,
        date = "N/A",
        modified = None,
        posts = removed_posts)  

    @authorizator.admin_required
    def create(self, name = "", email = ""):
        if request.method == "POST":
            mail = request.form.get("email")
            pwd = request.form.get("pwd")
            username = request.form.get("username")
            first_role = request.form.get("usr_role")
            print(first_role)
            if not self.__sign_up_validated(username, mail):
                return redirect(url_for(".create"))
            else:
                new_user = User(username, mail, role = first_role)
                new_user.password = self.hasher.generate_pass(pwd)
                new_user.id = self.users.add(new_user)
                signed_id = new_user.id
                if (name != ""):
                    return redirect(url_for("posts.unarchive", id = signed_id, name = username, email = email))
                return redirect(url_for(".user_profile", user_id = signed_id))
        return render_template("create_users.html", name = name, email = email)

    @authorizator.admin_required
    def activate(self, user_id):
        inactive = self.users.get_inactive(user_id)
        return redirect(url_for(".create", name = inactive.name, email = inactive.email))

    def __update_info(self, user_id):
        new_name = request.form.get("username")
        new_mail = request.form.get("email", user_id)
        new_password = self.__hash_if_new_pass(request.form.get("pwd"))
        new_role = request.form.get("usr_role")
        if self.active_usr.get_logged_user().role == "regular":
            self.active_usr.edit_logged(new_name, new_password)
        self.users.update(user_id, User(new_name, new_mail, role=new_role), new_password)

    def delete_user(self):
        to_delete = self.users.get_by(id = request.form.get("userID"))
        self.active_usr.log_out()
        flash(f"Your membership has been canceled.")
        self.users.remove(to_delete)

    def __hash_if_new_pass(self, input):
        if input != "":
            return self.hasher.generate_pass(input)
        return input

    def __sign_up_validated(self, name, email):
        if self.users.get_by(mail = email) != None:
            flash(f"Email {email} is already assigned to another user.")
            flash(f"Please use an unregistered email or if you have an account go to login.", "error")
            return False
        flash(f"Welcome, {name}!")
        flash("This is your profile page. Here you can see all of your posts.")
        flash("Select Create new post to add a new post", "info")
        return True

    def __is_editter(self, logged : Logged_user, usr_id = None) -> bool:
        is_admin : bool = logged.role in ("default", "admin")
        if usr_id == None:
            return is_admin
        return is_admin or usr_id == logged.id