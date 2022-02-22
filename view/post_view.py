from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.post import Post


class PostPage:
    def __init__(self, allPosts):
        self.blogPosts = allPosts
        self.bp = self.create_bp()           
                
    def create_bp(self):
        post = Blueprint("posts", __name__)
        @post.before_request
        def goto_db_setup():
            if str(type(self.blogPosts)).find("PostsDb") != -1 and self.blogPosts.db.current_config == None:
                return redirect(url_for("db_setup.set_database"))

        @post.route("/create", methods = ["Get", "Post"])
        def create():
            if request.method == "POST":
                self.create_new_post()
                return redirect(f"/post/read/{self.blogPosts.get_ids()[-1]}")

            return render_template("writePost.html")

        @post.route("/read/<post_id>",methods = ["Get", "Post"])
        def read(post_id):
            if request.method == "POST":
                to_delete = request.form.get("postID")
                self.blogPosts.remove(to_delete)
                flash("Your post has been successfully removed.", "info")
                return redirect(url_for("home.front_page"))
            
            selected_post = self.blogPosts.get_post(post_id)
            return render_template(
                "read.html",
                editable = post_id,
                title = selected_post.title,
                auth = selected_post.auth,
                content = selected_post.content,
                date = selected_post.date)

        @post.route("/edit/<post_id>", methods = ["Get", "Post"])
        def edit(post_id):
            selected_post = self.blogPosts.get_post(post_id)
            if request.method == "POST":
                self.edit_post(post_id)
                return redirect(f"/post/read/{post_id}")
            return render_template(
                "edit.html",
                auth = selected_post.auth,
                title = selected_post.title,
                current = selected_post.content,
                date = selected_post.date)
        return post
    
    def create_new_post(self):
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("post")
        self.blogPosts.add_post(Post(author, title, content))

    def edit_post(self, post_id):
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("post")
        editted = Post(author, title, content)
        self.blogPosts.replace(post_id, editted)
        
