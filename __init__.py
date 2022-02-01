from flask import Flask, Blueprint
from datetime import timedelta

def createBlog():
    blog = Flask(__name__)
    blog.config["Secret_key"]= "FlaskBlog"
    blog.permanent_session_lifetime= timedelta(hours = 1)

    from posts import posts
    blog.register_blueprint(posts, url_prefix="/")

    from account import profile
    blog.register_blueprint(profile, url_prefix="/")

    return blog