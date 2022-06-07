from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.post import Post
from services.database.database import DataBase
from services.interfaces.iauthorization import IAuthorization
from services.interfaces.ipost_repo import IPostRepo
from services.dependency_inject.injector import Services
from services.interfaces.isession_mngr import ISessionMNGR
from services.users.access_decorators import AccessDecorators

class PostPage:
    authorizator = AccessDecorators(IAuthorization, ISessionMNGR)

    @Services.get
    def __init__(self, repo : IPostRepo):
        self.blogPosts = repo
        self.bp = Blueprint("posts", __name__)
        self.to_db_setup = self.bp.before_request(self.goto_db_setup)
        self.creation = self.register("/create",self.create)
        self.reading = self.register("/read/<post_id>/", self.read)
        self.update = self.register("/edit/<post_id>", self.edit)
        self.activate_deleted = self.register("/unarchive/<id>/<name>/<email>", self.unarchive)

    def register(self, link, func):
        return self.bp.route(link, methods = ["Get", "Post"])(func)

    def goto_db_setup(self):
        if not DataBase.config.is_configured:
            return redirect(url_for("db_setup.set_database"))

    @authorizator.member_required
    def create(self):
        if request.method == "POST":
            id = self.create_new_post()
            return redirect(f"/post/read/{id}")
        
        return render_template("writePost.html", owner = session["username"])
        
    def read(self, post_id):
        email = request.args.get("email")
        selected_post = self.blogPosts.get(post_id, email)
        if request.method == "POST":
            to_delete = request.form.get("postID")
            self.blogPosts.remove(to_delete)
            flash("Your post has been successfully removed.", "info")
            return redirect(url_for("home.front_page"))
        
        return render_template(
            "read.html",
            editable=post_id,
            img = selected_post.img_path,
            owner = selected_post.owner_id,
            auth = selected_post.auth,
            title = selected_post.title,
            content = selected_post.content,
            created = selected_post.created,
            modified = selected_post.modified)

    @authorizator.owner_or_admin
    def edit(self, post_id):
        selected_post = self.blogPosts.get(post_id)
        if request.method == "POST":
            self.edit_post(selected_post)
            return redirect(f"/post/read/{post_id}")
        return render_template(
            "edit.html",
            owner = selected_post.auth,
            title = selected_post.title,
            current = selected_post.content,
            img = selected_post.img_path
            )

    def create_new_post(self):
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("post")
        image = request.files.get("img")
        return self.blogPosts.add(Post(author, title, content, owner_id = session["id"]), image)

    def edit_post(self, post : Post):
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("post")
        editted = Post(author, title, content)
        editted.id = post.id
        picture = request.files.get("img")
        if picture:
            editted.img_path = post.img_path
        self.blogPosts.replace(editted, picture)

    @authorizator.admin_required
    def unarchive(self, **kwargs):
        id = kwargs["id"]
        name = kwargs["name"]
        email = kwargs["email"]
        self.blogPosts.unarchive_content(id, name, email)
        return redirect(url_for("profile.user_profile", user_id = id, pg = 1, restored = email))
        