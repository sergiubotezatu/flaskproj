import unittest
from flask import current_app, url_for
from __initblog__ import create_blog
from services.database.database import DataBase
from services.users.passhash import PassHash

def log_user(id, name, email, role):
    def decorator(test_func):
        def wrapper(self):
            with self.test_app.session_transaction() as session:
                session["id"] = id
                session["username"] = name
                session["email"] = email
                session["role"] = role
            return test_func(self)
        return wrapper
    return decorator

def configure(is_config : bool):
    def decorator(test_func):
        def wrapper(self):
            DataBase.config.is_configured = is_config
            return test_func(self)
        return wrapper
    return decorator

class UsersTests(unittest.TestCase):
    blog = create_blog(is_test_app = True)
    
    def setUp(self):
        with self.blog.test_request_context() as self.ctx:
            self.test_app = current_app.test_client()
            self.ctx.push()

    @configure(True)
    def test_create_user(self):
        user = {
        "username" : "John Doe",
        "email" : "JDoe@John",
        "pwd" : "password1@"
        }        
        
        creation = self.test_app.post("/signup", data = user, follow_redirects=True)
        self.assertIn(user["username"], creation.data.decode("UTF-8"))
        self.assertIn(user["email"], creation.data.decode("UTF-8"))
    
    @log_user(2, "John Doe", "JDoe@John", "regular")
    @configure(True)
    def test_delete_user(self):
        read_user = self.test_app.get("view/2")
        self.assertIn("John Doe", read_user.data.decode("UTF-8"))
        result = self.test_app.post("view/2", data = {"userID" : "2"}, follow_redirects = False)
        self.assertEqual("/", result.location)
        self.assertNotIn("John Doe", result.data.decode("UTF-8"))

    @configure(True)
    def test_create_redirects_to_profile(self):
        user = {
        "username" : "Mark Doe",
        "email" : "MDoe@John",
        "pwd" : "password1@"
        }
        creation = self.test_app.post("/signup", data = user, follow_redirects=False)
        self.assertEqual(creation.location, url_for("profile.user_profile", user_id = 1))

    @log_user(1, "Mark Doe", "JDoe@John", "regular")
    @configure(True)
    def test_edit_user(self):
        edit = {
        "username" : "James Doe",
        "email" : "MDoe@John",
        "pwd" : "password1@",
        "oldpass" : "password1@"
        }       
        
        self.test_app.post("/edit/1", data = edit, follow_redirects=True)
        result = self.test_app.get("/view/1")
        self.assertIn(edit["username"], result.data.decode("UTF-8"))

    @configure(True)
    def test_read_user(self):
        read_user = self.test_app.get("/view/1")
        self.assertIn("James Doe", read_user.data.decode("UTF-8"))

if __name__ == "__main__":
    unittest.main()