import unittest
from flask import current_app
from __initblog__ import create_blog
from services.database.database import DataBase
from services.users.passhash import PassHash

def configure(is_config = True):
    def decorator(test_func):
        def wrapper(self):
            DataBase.config.is_configured = is_config
            test_func(self)
        return wrapper
    return decorator

class UsersTests(unittest.TestCase):
    blog = create_blog(is_test_app = True)
    
    def setUp(self):
        with self.blog.test_request_context() as self.ctx:
            self.test_app = current_app.test_client()
            self.ctx.push()

    @configure
    def test_create_user(self):
        user = {
        "username" : "John Doe",
        "email" : "JDoe@John",
        "pwd" : "password1@"
        }        
        
        creation = self.test_app.post("/signup", data = user, follow_redirects=True)
        self.assertIn(user["username"], creation.data.decode("UTF-8"))
        self.assertIn(user["email"], creation.data.decode("UTF-8"))

    @configure
    def test_password_hashing(self):
        user = {
        "username" : "John Doe",
        "email" : "JDoe@John",
        "pwd" : "password1@"
        }        
        
        hashed_pass = PassHash.generate_pass("password1@")
        creation = self.test_app.post("/signup", data = user, follow_redirects=True)
        self.assertNotIn(user["pwd"], creation.data.decode("UTF-8"))
        self.assertIn(hashed_pass, creation.data.decode("UTF-8"))