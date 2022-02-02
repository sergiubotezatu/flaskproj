from flask import Flask, Blueprint

def createBlog():
    blog = Flask(__name__)
    blog.config["Secret_key"]= "FlaskBlog"
    
    from view.allPosts import allPosts
    blog.register_blueprint(allPosts, url_prefix="/")

    from view.individPost import post
    blog.register_blueprint(post, url_prefix="/post")

    return blog