from flask import Flask
from services.interfaces.Ipassword_hash import IPassHash
from services.interfaces.iauthentication import IAuthentication
from services.interfaces.idata_base import IDataBase
from services.dependency_inject.injector import Services
from services.dependency_inject.container import Container
from services.interfaces.ifilters import IFilters
from services.interfaces.ipost_repo import IPostRepo
from services.interfaces.isession_mngr import ISessionMNGR
from services.interfaces.iusers_repo import IUsersRepo
from datetime import timedelta
from services.users.users_db_repo import UsersDb


def create_blog(is_test_app = False, with_orm = True):
    blog = Flask(__name__)
    blog.config["TESTING"] = is_test_app
    blog.permanent_session_lifetime = timedelta(days = 1)
    blog.secret_key = "FlaskTest" if is_test_app else "FlaskBlog"
    Services.container = Container(is_test_app).items
    Services.dependencies = Container.dependencies
    from view.db_setup import DbSetUp
    with blog.app_context():
        blog.register_blueprint(DbSetUp(IDataBase, with_orm).bp)
    from view.home import Home
    blog.register_blueprint(Home(IFilters).bp, url_prefix="/")
    from view.post_view import PostPage
    blog.register_blueprint(PostPage(IPostRepo).bp, url_prefix="/post")
    from view.user_profile import UserProfile
    blog.register_blueprint(UserProfile(IUsersRepo, IPassHash, ISessionMNGR, IFilters).bp)
    from view.user_authenticate import UserAuthenticate
    blog.register_blueprint(UserAuthenticate(IAuthentication).bp)

    return blog
