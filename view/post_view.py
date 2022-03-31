from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.post import Post
from services.database import DataBase
from services.ipost_repo import IPostRepo
from services.resources import Services
from services.authorization import Authorization
from services.authentication import Authentication
from services.access_decorators import decorator, member_required, owner_or_admin

class PostPage:
    @Services.get
    def __init__(self, repo : IPostRepo):
        self.blogPosts = repo
        self.bp = Blueprint("posts", __name__)
        self.to_db_setup = self.bp.before_request(self.goto_db_setup)
        self.creation = self.register("/create",self.create)
        self.reading = self.register("/read/<post_id>", self.read)
        self.update = self.register("/edit/<post_id>", self.edit)

    def register(self, link, func):
        return self.bp.route(link, methods = ["Get", "Post"])(func)

    @decorator.only_once
    def goto_db_setup(self):
        return redirect(url_for("db_setup.set_database"))

    @member_required
    def create(self):
        if request.method == "POST":
            return redirect(f"/post/read/{self.create_new_post()}")
        
        return render_template("writePost.html", owner = session["username"])
        
    def read(self, post_id):
        if request.method == "POST":
            to_delete = request.form.get("postID")
            self.blogPosts.remove(to_delete)
            flash("Your post has been successfully removed.", "info")
            return redirect(url_for("home.front_page"))
        
        selected_post = self.blogPosts.get_post(post_id)
        return render_template(
            "read.html",
            editable = post_id,
            owner = selected_post.owner_id,
            auth = selected_post.auth,
            title = selected_post.title,
            content = selected_post.content,
            created = selected_post.created,
            modified = selected_post.modified)

    @owner_or_admin
    def edit(self, post_id):
        selected_post = self.blogPosts.get_post(post_id)
        if request.method == "POST":
            self.edit_post(post_id)
            return redirect(f"/post/read/{post_id}")
        return render_template(
            "edit.html",
            owner = selected_post.auth,
            title = selected_post.title,
            current = selected_post.content
            )

    def create_new_post(self):
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("post")
        return self.blogPosts.add_post(Post(author, title, content, owner_id = session["id"]))

    def edit_post(self, post_id):
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("post")
        editted = Post(author, title, content)
        self.blogPosts.replace(post_id, editted)