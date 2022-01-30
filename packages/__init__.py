from flask import Flask

def createBlog():
    blog = Flask(__name__)
    blog.config["Secret_key"]= "FlaskBlog"

    from .posts import posts
    blog.register_blueprint(posts, url_prefix="/")

    from .profile import profile
    blog.register_blueprint(profile, url_prefix="/")

    return blog