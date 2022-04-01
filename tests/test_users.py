import unittest

from flask import current_app
from __initblog__ import create_blog


class UsersTests(unittest.TestCase):
    blog = create_blog(is_test_app = True)
    
    def setUp(self):
        with self.blog.test_request_context() as self.ctx:
            self.test_app = current_app.test_client()
            self.ctx.push()

    def test_create_user(self):
        user = {
        "username" : "John Doe",
        "email" : "JDoe@John",
        "pwd" : "password1@"
        }

        from services.access_decorators import decorator
        decorator.redirects = 1
        creation = self.test_app.post("/signup", data = user, follow_redirects=False)
        self.assertIn(creation["username"], creation.data.decode("UTF-8"))
        self.assertIn(creation["email"], creation.data.decode("UTF-8"))
        self.assertIn(creation["pwd"], creation.data.decode("UTF-8"))
        

        
