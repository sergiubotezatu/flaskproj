from functools import wraps
from services.dependency_inject.injector import Services
from services.interfaces.iauthorization import IAuthorization
from flask import redirect, url_for

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
                    return redirect(url_for("authentication.log_in"))
        return wrapper
        
    def owner_or_admin(self, routing):
        @wraps(routing)
        def wrapper(instance, **Kwargs):
                if self.authorizator.is_owner_or_admin(instance, **Kwargs):
                    return routing(instance, **Kwargs)
                else:
                    return "<h1>you do not have the necessary autorization.</h1>"
        return wrapper
            
    def admin_required(self, routing):
        @wraps(routing)
        def wrapper(instance, **kwargs):
            if self.authorizator.is_admin():
                return routing(instance, **kwargs)
            else:
                return "<h1>you do not have the necessary autorization.</h1>"
        return wrapper
