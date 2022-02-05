from flask import Flask, Blueprint

def createBlog():
    blog = Flask(__name__)
    blog.config["Secret_key"]= "FlaskBlog"
    
    from view.Home import home
    blog.register_blueprint(home, url_prefix="/")

    from view.PostView import post
    blog.register_blueprint(post, url_prefix="/post")

    return blog