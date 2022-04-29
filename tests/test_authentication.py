import unittest
from urllib.parse import urlparse
from flask import current_app, url_for
from __initblog__ import create_blog
from models.post import Post
from models.user import User
from services.database.database import DataBase

def log_user(id, name, email, role):
    def decorator(test_func):
        def wrapper(self):
            with self.test_app.session_transaction() as session:
                session["id"] = str(id)
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

class AuthenticationTests(unittest.TestCase):
    blog = create_blog(is_test_app = True)
    
    def setUp(self):
        with self.blog.test_request_context() as self.ctx:
            self.test_app = current_app.test_client()
            self.ctx.push()

    def create_user(self):
        user = {
                "username" : "John Doe",
                "email" : "JDoe@mail",
                "pwd" : "password1@"
                }
        self.test_app.post("/signup", data = user, follow_redirects=False)

    USER = {
        "mail" : "JDoe@mail",
        "pwd" : "password1@",
        }

    @configure(False)
    def test_redirects_tosetup_if_notConfig(self):
        result = self.test_app.get("/login", follow_redirects = True)
        self.assertIn("host", result.data.decode("UTF-8"))

    @configure(True)
    def test_login_request(self):
        result = self.test_app.get("/login")
        self.assertEqual(result.status_code, 200)

    @log_user(1, "John Doe", "JDoe@mail", "regular")
    @configure(True)
    def test_login_redirect_if_already_logged(self):
        with self.test_app.session_transaction():
            login = self.test_app.post("/login", data = self.USER, follow_redirects=False)
            result = self.test_app.get(login.location)
            self.assertEqual(urlparse(login.location).path, url_for("profile.user_profile", user_id = 1))
            self.assertIn("You are already logged", result.data.decode("UTF-8"))

    @log_user(1, "John Doe", "JDoe@mail", "regular")
    @configure(True)
    def test_logout_pops_user_from_session(self):
        with self.test_app.session_transaction() as session:
            self.assertEqual(session["id"], "1")
        self.test_app.get(url_for("authentication.log_out"))
        with self.test_app.session_transaction() as session:
            self.assertNotIn("id", session)

    @configure(True)
    def test_login_adds_user_into_session(self):
        self.create_user()
        self.test_app.get(url_for("authentication.log_out"))
        self.test_app.post("/login", data = self.USER, follow_redirects=True)
        with self.test_app.session_transaction() as session:
            self.assertEqual(session["id"], "1")
            self.assertEqual(session["username"], "John Doe")
            self.assertEqual(session["email"], "JDoe@mail")
            self.assertEqual(session["role"], "regular")

    @configure(True)
    def test_login_fails_wrong_email(self):
        wrong_mail = {
        "mail" : "JDoe@gmail",
        "pwd" : "password1@",
        }
        login = self.test_app.post("/login", data = wrong_mail, follow_redirects=False)
        result = self.test_app.get(login.location)
        self.assertEqual(urlparse(login.location).path, "/login")
        self.assertIn("Incorrect Password or Email. Please try again", result.data.decode("UTF-8"))

    @configure(True)
    def test_login_fails_wrong_password(self):
        wrong_pass = {
        "mail" : "JDoe@gmail",
        "pwd" : "password1@",
        }
        login = self.test_app.post("/login", data = wrong_pass, follow_redirects=False)
        result = self.test_app.get(login.location)
        self.assertEqual(urlparse(login.location).path, "/login")
        self.assertIn("Incorrect Password or Email. Please try again", result.data.decode("UTF-8"))

    @configure(True)
    def test_user_displayed_on_navbar(self):
        self.test_app.post("/login", data = self.USER, follow_redirects=False)
        home = self.test_app.get("/")
        self.assertIn("John Doe", home.data.decode("UTF-8"))