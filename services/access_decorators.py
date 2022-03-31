from functools import wraps
from services.authorization import Authorization
from services.iauthentication import IAuthentication
from flask import redirect, url_for

authorizator = Authorization(IAuthentication)

def member_required(routing):
    @wraps(routing)
    def wrapper(*args, **Kwargs):
            if authorizator.is_member():
                return routing(*args, **Kwargs)
            else:
                return redirect(url_for("authentication.log_in"))
    return wrapper
        
def owner_or_admin(routing):
    @wraps(routing)
    def wrapper(instance, **Kwargs):
            if authorizator.is_owner_or_admin(instance, **Kwargs):
                return routing(instance, **Kwargs)
            else:
                return "<h1>you do not have the necessary autorization.</h1>"
    return wrapper
        
def admin_required(routing):
    @wraps(routing)
    def wrapper(instance, **kwargs):
        if authorizator.is_admin():
            return routing(instance, **kwargs)
        else:
            return "<h1>you do not have the necessary autorization.</h1>"
    return wrapper

class decorator:
    redirects = 0

    def only_once(redirecter):
        def wrapper(instance):
            if decorator.redirects == 0:
                decorator.redirects = 1
                return redirecter(instance)
        return wrapper
