from flask import Flask
from services.posts_factory import Create
from services.seed import blogPosts

def create_blog(is_test_app = False):
    blog = Flask(__name__)
    blog.config["TESTING"] = is_test_app
    blog.secret_key = "FlaskTest" if is_test_app else "FlaskBlog"
        
    from view.home import Home
    front_page = Home(Create(is_test_app))
    blog.register_blueprint(front_page.bp, url_prefix="/")
    from view.post_view import PostPage
    post_page = PostPage(front_page.blogPosts)
    blog.register_blueprint(post_page.bp, url_prefix="/post")

    return blog
