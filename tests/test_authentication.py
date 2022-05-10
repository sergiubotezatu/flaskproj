import unittest
from urllib.parse import urlparse
from flask import current_app, url_for
from __initblog__ import create_blog
from models.post import Post
from models.user import User
from services.database.database import DataBase
from services.interfaces.iusers_repo import IUsersRepo
from tests.test_helpers import RepoMngr, log_user, configure, create_user

class AuthenticationTests(unittest.TestCase):
    blog = create_blog(is_test_app = True, with_orm=False)
    
    def setUp(self):
        with self.blog.test_request_context() as self.ctx:
            self.test_app = current_app.test_client()
            self.ctx.push()

    USER = {
        "mail" : "JDoe@mail",
        "pwd" : "password1@",
        }

    users = RepoMngr(IUsersRepo)

    @configure(False)
    def test_redirects_tosetup_if_notConfig(self):
        result = self.test_app.get("/login", follow_redirects = True)
        self.assertIn("host", result.data.decode("UTF-8"))

    @configure(True)
    def test_login_request(self):
        result = self.test_app.get("/login")
        self.assertEqual(result.status_code, 200)

    @configure(True)
    def test_login_redirect_if_already_logged(self):
        create_user(self, "John Doe", "JDoe@mail")
        login = self.test_app.post("/login", data = self.USER, follow_redirects=False)
        result = self.test_app.get(login.location)
        self.assertEqual(urlparse(login.location).path, url_for("profile.user_profile", user_id = 1))
        self.assertIn("You are already logged", result.data.decode("UTF-8"))
        self.users.delete(1)

    @log_user(1, "John Doe", "JDoe@mail", "regular")
    @configure(True)
    def test_logout_pops_user_from_session(self):
        with self.test_app.session_transaction() as session:
            self.assertEqual(session["id"], 1)
        self.test_app.get(url_for("authentication.log_out"))
        with self.test_app.session_transaction() as session:
            self.assertNotIn("id", session)

    @configure(True)
    def test_login_adds_user_into_session(self):
        create_user(self, "John Doe", "JDoe@mail")
        self.test_app.get(url_for("authentication.log_out"))
        self.test_app.post("/login", data = self.USER, follow_redirects=False)
        with self.test_app.session_transaction() as session:
            self.assertEqual(session["id"], 1)
            self.assertEqual(session["username"], "John Doe")
            self.assertEqual(session["email"], "JDoe@mail")
            self.assertEqual(session["role"], "regular")
        self.users.delete(1)
       
    @configure(True)
    def test_login_fails_wrong_email(self):
        create_user(self, "John Doe", "John@mail")
        wrong_mail = {
        "mail" : "JDoe@gmail",
        "pwd" : "password1@",
        }
        self.test_app.get(url_for("authentication.log_out"))
        login = self.test_app.post("/login", data = wrong_mail, follow_redirects=True)
        self.assertIn("Incorrect Password or Email. Please try again", login.data.decode("UTF-8"))
        self.users.delete(1)

    @configure(True)
    def test_login_fails_wrong_password(self):
        create_user(self, "John Doe", "John@mail")
        wrong_pass = {
        "mail" : "John@mail",
        "pwd" : "pass1@",
        }
        self.test_app.get(url_for("authentication.log_out"))
        login = self.test_app.post("/login", data = wrong_pass, follow_redirects=False)
        self.assertIn("Incorrect Password or Email. Please try again", login.data.decode("UTF-8"))
        self.users.delete(1)

    @configure(True)
    def test_user_displayed_on_navbar(self):
        create_user(self, "John Doe", "J@mail")
        self.test_app.post("/login", data = self.USER, follow_redirects=False)
        home = self.test_app.get("/")
        self.assertIn("John Doe", home.data.decode("UTF-8"))
        self.users.delete(1)