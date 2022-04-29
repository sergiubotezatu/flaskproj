from functools import wraps
from services.dependency_inject.injector import Services
from services.interfaces.iauthorization import IAuthorization
from flask import flash, redirect, render_template, url_for

class AccessDecorators:
    @Services.get
    def __init__(self, authorizator : IAuthorization):
        self.authorizator = authorizator

    def member_required(self, routing):
        @wraps(routing)
        def wrapper(*args, **Kwargs):
                if self.authorizator.is_member():
                    return routing(*args, **Kwargs)
                else:
                    return render_template("forbidden.html", error = "403", role = "members")
        return wrapper
        
    def owner_or_admin(self, routing):
        @wraps(routing)
        def wrapper(instance, **Kwargs):
                if self.authorizator.is_owner_or_admin(instance, **Kwargs):
                    return routing(instance, **Kwargs)
                else:
                    return render_template("forbidden.html", error = "405", role = "admins")
        return wrapper
            
    def admin_required(self, routing):
        @wraps(routing)
        def wrapper(instance, **kwargs):
            if self.authorizator.is_admin():
                return routing(instance, **kwargs)
            else:
                return render_template("forbidden.html", error = "403", role = "admins")
        return wrapper

    def logged_not_allowed(self, routing):
        @wraps(routing)
        def wrapper(*args, **Kwargs):
                if self.authorizator.is_member():
                    logged = self.authorizator.authenticator.get_logged_user()
                    flash(f"You are already logged in with name {logged.name}")
                    flash(f"If you want to log in with a different account, log out first.")
                    return redirect(url_for("profile.user_profile", user_id = logged.id, pg = ["1"]))
                else:
                    return routing(*args, **Kwargs)
        return wrapper
