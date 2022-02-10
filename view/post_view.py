from flask import Blueprint, render_template, request, redirect, url_for, flash
from postRepo.seed import blogPosts
from models.post import Post

post = Blueprint("posts", __name__)

@post.route("/create", methods = ["Get", "Post"])
def create():
    if request.method == "POST":
        create_new_post()
        return redirect(f"/post/read/post_id_{blogPosts.get_ids()[-1]}")

    return render_template("writePost.html")

@post.route("/read/post_id_<post_id>",methods = ["Get", "Post"])
def read(post_id):
    if request.method == "POST":
        to_delete = request.form.get("action")
        blogPosts.remove(to_delete)
        flash("Your post has been successfully removed.", "info")
        return redirect(url_for("home.front_page"))
    else:
        selected_post = blogPosts.get_post(post_id)
        return render_template(
            "read.html",
            editable = post_id,
            title = selected_post.title,
            auth = selected_post.auth,
            content = selected_post.content,
            date = selected_post.date)

@post.route("/edit/post_id_<post_id>", methods = ["Get", "Post"])
def edit(post_id):
    selected_post = blogPosts.get_post(post_id)
    if request.method == "POST":
        edit_post(post_id)
        return redirect(f"/post/read/post_id_{post_id}")
    return render_template(
        "edit.html",
        auth = selected_post.auth,
        title = selected_post.title,
        current = selected_post.content,
        date = selected_post.date)

def create_new_post():
    author = request.form.get("author")
    title = request.form.get("title")
    content = request.form.get("post")
    blogPosts.add_post(Post(author, title, content))

def edit_post(post_id):
    author = request.form.get("author")
    title = request.form.get("title")
    content = request.form.get("post")
    editted = Post(author, title, content)
    blogPosts.replace(post_id, editted)
   