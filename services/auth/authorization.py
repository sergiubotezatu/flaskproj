from functools import wraps
from flask import redirect, url_for
from models.user import User
from services.interfaces.iauthentication import IAuthentication
from services.dependency_inject.injector import Services

class Authorization:
    @Services.get
    def __init__(self, authenticator : IAuthentication):
        self.authenticator = authenticator    

    def is_owner(self, posts_instance, **kwargs):
        logged = self.authenticator.get_logged_user()
        if logged == None:
            return False
        else:
            logged_id = logged.id
        
        if "post_id" in kwargs:
            post_id = kwargs["post_id"]
            owner_id = posts_instance.blogPosts.get(post_id).owner_id
            return logged_id == owner_id
        if "user_id" in kwargs:
            print(kwargs["user_id"])
            print(logged_id)
            return logged_id == int(kwargs["user_id"])

    def is_admin(self):
        logged = self.authenticator.get_logged_user()
        if logged != None:
            return logged.role == "admin" or logged.role == "default"
        return False

    def is_owner_or_admin(self, posts_instance, **kwargs):
        return self.is_admin() or self.is_owner(posts_instance, **kwargs)

    def is_default_admin(self, logged_user: User):
        return logged_user.role == "default"

    def is_member(self):
        return self.authenticator.get_logged_user() != None
