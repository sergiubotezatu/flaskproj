from flask import Blueprint, render_template, url_for, redirect, request, session, flash
from models.logged_user import Logged_user
from services.database.database import DataBase
from services.interfaces.iauthorization import IAuthorization
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
        self.activate_old = self.register("/activate/<mail>", self.activate)
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
                return render_template("signup.html", usrname = username)
            else:
                new_user = User(username, email)
                new_user.password = self.hasher.generate_pass(pwd)
                new_user.id = self.users.add(new_user)
                self.active_usr.log_session(new_user.id, username, email, new_user.role)
                return redirect(url_for(".user_profile", user_id = new_user.id, pg = ["1"]))
        return render_template("signup.html")

    @authorizator.member_required
    def user_profile(self, user_id):
        self.__remove_restored()
        if request.method == "POST":
            self.delete_user()
            return redirect(url_for("home.front_page"))
        displayed = self.users.get_by(id = user_id)
        filter_params = {"user_id" : [user_id], "name" : [displayed.name]}
        page = int(request.args.get("pg"))
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
        user_id = user_id
        editable : User = self.users.get_by(id = user_id)
        if request.method == "POST":
            identity_checker = request.form.get("oldpass")
            if identity_checker == "" or self.hasher.check_pass(editable.hashed_pass, identity_checker) :
                self.__update_info(user_id)
                return redirect(url_for(".user_profile", user_id = user_id, pg = ["1"]))
            else:
                flash(f"Old password does not match current one. Please try again", "error")
        
        return render_template("edit_user.html",
                                is_admin = self.__is_editter(self.active_usr.get_logged_user()),
                                username = editable.name,
                                email = editable.email,
                                role = editable.role)

    @authorizator.admin_required
    def get_all_users(self):
        params = request.args.getlist("usr_role")
        if params == []:
            return render_template("members.html", allmembers = self.users.get_all(not_filtered = True))
        return self.__render_filtered_users(params)

    @authorizator.admin_required
    def inactive_user(self, email):
        if request.method == "POST":
            self.delete_user()
            return redirect(url_for("home.front_page"))
        removed_posts = self.users.get_inactive_posts(email)
        return render_template("user.html", 
                                user_id = email,
                                user= "Deleted User",
                                name = email,
                                email = email,
                                date = "N/A",
                                modified = None,
                                posts = removed_posts,
                                pg = 1,
                                edit_allowed = True)  

    @authorizator.admin_required
    def create(self, name = "", email = ""):
        if request.method == "POST":
            mail = request.form.get("email")
            pwd = request.form.get("pwd")
            username = request.form.get("username")
            first_role = request.form.get("usr_role")
            if not self.__sign_up_validated(username, mail):
                return redirect(url_for(".create"))
            else:
                new_user = User(username, mail, role = first_role)
                new_user.password = self.hasher.generate_pass(pwd)
                new_user.id = self.users.add(new_user)
                signed_id = new_user.id
                if (name != ""):
                    session.pop("__flashes")
                    return redirect(url_for("posts.unarchive", id = signed_id, name = username, email = email))
                return redirect(url_for(".user_profile", user_id = signed_id, pg = ["1"]))
        return render_template("create_users.html", name = name, email = email)

    @authorizator.admin_required
    def activate(self, mail):
        inactive_name = mail[0:mail.index("@")]
        return redirect(url_for(".create", name = inactive_name, email = mail))

    def __update_info(self, user_id):
        new_name = request.form.get("username")
        new_mail = request.form.get("mail")
        new_password = self.__hash_if_new_pass(request.form.get("pwd"))
        new_role = request.form.get("usr_role")
        if self.active_usr.get_logged_user().id == int(user_id):
            self.active_usr.edit_logged(new_name, new_mail, new_role)
        self.users.update(user_id, User(new_name, new_mail, role=new_role), new_password)

    def delete_user(self):
        logged = self.active_usr.get_logged_user()
        message = "membership has been canceled."
        to_delete = request.form.get("userID")
        if logged.role not in ("admin, default"):
            self.active_usr.log_out()
            message = "Your " + message
        flash(message)
        self.users.remove(to_delete)

    def __hash_if_new_pass(self, input):
        if input != "":
            return self.hasher.generate_pass(input)
        return input

    def __sign_up_validated(self, name, email):
        if self.users.has_account(email):
            flash(f"Email {email} is already assigned to another user.")
            flash(f"Please use an unregistered email or if you have an account go to login.", "error")
            return False
        flash(f"Welcome, {name}!")
        flash("This is your profile page. Here you can see all of your posts.")
        flash("Select Create new post to add yout first post", "info")
        return True

    def __is_editter(self, logged : Logged_user, usr_id = None) -> bool:
        is_admin : bool = logged.role in ("default", "admin")
        if usr_id == None:
            return is_admin
        return is_admin or int(usr_id) == logged.id

    def __render_filtered_users(self, query_params):
        where_clause = ""
        inactive_needed = False
        param_count = len(query_params)
        if "deleted" in query_params:
            inactive_needed = True
            query_params.pop(param_count - 1)
            param_count -= 1
        if param_count > 1:
            where_clause += f"Where u.role IN ({query_params[0]}, {query_params[1]})"
        elif param_count ==  1:
            where_clause += f"Where u.role IN ({query_params[0]})"
        return render_template("members.html", allmembers = self.users.get_all(where_clause, inactive_needed))

    def __remove_restored(self):
        email = request.args.get("restored")
        if email != None:
            self.users.remove(email)
        