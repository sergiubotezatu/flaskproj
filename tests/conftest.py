import sys
from os.path import dirname as dir
from os.path import abspath
from pytest import fixture
from models.post import Post
from models.user import User
from flask import Flask
from services.posts.posts_in_memo import Posts
from services.users.passhash import PassHash
from services.users.users_in_memo import Users
import __init__

root_dir = dir(dir(abspath(__file__)))
sys.path.append(root_dir)

def create_user_db(repo : Users, user_info : list[tuple[str]]):
    for info in user_info:
        user = User(info[0], info[1])
        user.hashed_pass = PassHash.generate_pass("password1@")
        repo.add(user)

def create_posts_db(repo: Posts, user_info : list[tuple[str]], count : int):
    for info in user_info:
        for i in range(count):
            post = Post(info[0], "Generic", f"Test post {str(i + 1)}", info[2])
            repo.add(post)

@fixture(scope="session")
def data_base() -> Flask:
    app = __init__.create_blog(is_test_app=True, with_orm=False)
    posts_db = Posts()
    users_db = Users()
    users = [("Mark Doe", "Mark@mail", 1), ("John Doe", "John@mail", 2)]
    create_user_db(users_db, users)
    create_posts_db(posts_db, users, 3)
    return app