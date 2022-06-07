import unittest
from flask.testing import FlaskClient
from flask import url_for
from __initblog__ import create_blog
from services.interfaces.iusers_repo import IUsersRepo
from tests.test_helpers import RepoMngr, log_user, configure, create_user, getClient

class AuthenticationTests(unittest.TestCase):
    USER = {
        "mail" : "JDoe@mail",
        "pwd" : "password1@",
        }
    
    
    @getClient
    @configure(False)
    def test_redirects_tosetup_if_notConfig(self, client : FlaskClient = None):
        result = client.get("/login", follow_redirects = True)
        self.assertIn("host", result.data.decode("UTF-8"))

    @getClient
    @configure(True)
    def test_login_request(self, client : FlaskClient = None):
        result = client.get("/login")
        self.assertEqual(result.status_code, 200)

    @getClient
    @configure(True)
    def test_login_redirect_if_already_logged(self, client : FlaskClient = None):
        create_user(client, "John Doe", "JDoe@mail")
        login = client.post("/login", data = self.USER, follow_redirects=False)
        result = client.get(login.location)
        self.assertIn("You are already logged", result.data.decode("UTF-8"))

    @getClient
    @log_user(1, "John Doe", "JDoe@mail", "regular")
    @configure(True)
    def test_logout_pops_user_from_session(self, client : FlaskClient = None):
        with client.session_transaction() as session:
            self.assertEqual(session["id"], 1)
        client.get("/logout")
        with client.session_transaction() as session:
            self.assertNotIn("id", session)

    @getClient
    @configure(True)
    def test_login_adds_user_into_session(self, client : FlaskClient = None):
        create_user(client, "John Doe", "JDoe@mail")
        client.get("/logout")
        client.post("/login", data = self.USER, follow_redirects=False)
        with client.session_transaction() as session:
            self.assertEqual(session["id"], 1)
            self.assertEqual(session["username"], "John Doe")
            self.assertEqual(session["email"], "JDoe@mail")
            self.assertEqual(session["role"], "regular")

    @getClient
    @configure(True)
    def test_login_fails_wrong_email(self, client : FlaskClient = None):
        create_user(client, "John Doe", "John@mail")
        wrong_mail = {
        "mail" : "JDoe@gmail",
        "pwd" : "password1@",
        }
        client.get("/logout")
        login = client.post("/login", data = wrong_mail, follow_redirects=True)
        self.assertIn("Incorrect Password or Email. Please try again", login.data.decode("UTF-8"))
    
    @getClient
    @configure(True)
    def test_login_fails_wrong_password(self, client : FlaskClient = None):
        create_user(client, "John Doe", "John@mail")
        wrong_pass = {
        "mail" : "John@mail",
        "pwd" : "pass1@",
        }
        client.get("/logout")
        login = client.post("/login", data = wrong_pass, follow_redirects=False)
        self.assertIn("Incorrect Password or Email. Please try again", login.data.decode("UTF-8"))
        
    @getClient
    @configure(True)
    def test_user_displayed_on_navbar(self, client : FlaskClient = None):
        create_user(client, "John Doe", "J@mail")
        client.post("/login", data = self.USER, follow_redirects=False)
        home = client.get("/")
        self.assertIn("John Doe", home.data.decode("UTF-8"))
