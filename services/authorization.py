from functools import wraps
from flask import redirect, url_for, session
from models.post import Post
from models.user import User
from services.Ipassword_hash import IPassHash
from services.iauthentication import IAuthentication
from services.authentication import Authentication
from services.resources import Services

class Authorization:
    @staticmethod
    def member_required(routing):
        @wraps(routing)
        def wrapper(*args, **Kwargs):
                if Authentication.is_any_logged_in():
                    return routing(*args, **Kwargs)
                else:
                    return redirect(url_for("authentication.log_in"))
        return wrapper
        
    @staticmethod
    def owner_or_admin(routing):
        @wraps(routing)
        def wrapper(instance, **Kwargs):
                if Authorization.is_owner_or_admin(instance, **Kwargs):
                    return routing(instance, **Kwargs)
                else:
                    return "<h1>you do not have the necessary autorization.</h1>"
        return wrapper
        
    @staticmethod
    def admin_required(routing):
        @wraps(routing)
        def wrapper(instance, **kwargs):
            if Authorization.is_admin():
                return routing(instance, **kwargs)
            else:
                return "<h1>you do not have the necessary autorization.</h1>"
        return wrapper
        

    @staticmethod
    def is_owner(posts_instance, **kwargs):
        if "id" not in session:
            return False
        else:
            logged_id = session["id"]
        
        if "post_id" in kwargs:
            post_id = kwargs["post_id"]
            owner_id = posts_instance.blogPosts.get_post(post_id).owner_id
            return logged_id == owner_id
        if "user_id" in kwargs:
            print(kwargs["user_id"])
            print(logged_id)
            return logged_id == int(kwargs["user_id"])

    @staticmethod
    def is_admin():
        if "email" in session:
            return session["email"][-6:] == "@admin"

    @staticmethod
    def is_owner_or_admin(posts_instance, **kwargs):
        return Authorization.is_admin() or Authorization.is_owner(posts_instance, **kwargs)

    @staticmethod
    def is_default_admin(logged_user: User):
        return Authorization.is_admin(logged_user) and logged_user.id == 1
