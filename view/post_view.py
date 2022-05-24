import base64
from models.image import Image
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.post import Post
from services.database.database import DataBase
from services.interfaces.iauthorization import IAuthorization
from services.interfaces.ipost_repo import IPostRepo
from services.dependency_inject.injector import Services
from services.interfaces.isession_mngr import ISessionMNGR
from services.users.access_decorators import AccessDecorators
from werkzeug.utils import secure_filename

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
        if request.method == "POST":
            picture = request.files.get("img")
            if picture:
                mimetype = picture.mimetype
                self.blogPosts.replace(post_id, img = Image(picture.read(), mimetype))
                return redirect(url_for(".read", post_id = post_id))
            else:
                to_delete = request.form.get("postID")
                self.blogPosts.remove(to_delete)
                flash("Your post has been successfully removed.", "info")
                return redirect(url_for("home.front_page"))
        
        email = request.args.get("email")
        selected_post = self.blogPosts.get(post_id, email)
        pic = base64.b64encode(self.blogPosts.get_img(post_id)).decode()
        return render_template(
            "read.html",
            editable=post_id,
            img = pic,
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
        image = self.__get_img()
        return self.blogPosts.add(Post(author, title, content, owner_id = session["id"]), image)

    def edit_post(self, post_id):
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("post")
        editted = Post(author, title, content)
        self.blogPosts.replace(post_id, editted)

    @authorizator.admin_required
    def unarchive(self, **kwargs):
        id = kwargs["id"]
        name = kwargs["name"]
        email = kwargs["email"]
        self.blogPosts.unarchive_content(id, name, email)
        return redirect(url_for("profile.user_profile", user_id = id, pg = 1, restored = email))

    def __get_img(self) -> Image:
        picture = request.files.get("img")
        if not picture:
            return Image.default()
        else:
            mimetype = picture.mimetype
            return Image(picture.read(), mimetype)

    
        