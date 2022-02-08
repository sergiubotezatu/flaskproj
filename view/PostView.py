from flask import Blueprint, render_template, request, redirect, url_for, flash
from postRepo.seed import blogPosts
from models.post import Post

post = Blueprint("posts", __name__)

@post.route("/create", methods = ["Get", "Post"])
def create():
    if request.method == "POST":
        createNewPost()
        return redirect("/post/read/id={}".format(blogPosts.getIds()[-1]))

    return render_template("writePost.html")

@post.route("/read/id=<postId>",methods = ["Get", "Post"])
def read(postId):
    if request.method == "POST":
        toDelete = request.form.get("action")
        blogPosts.remove(toDelete)
        flash("Your post has been successfully removed.", "info")
        return redirect(url_for("home.frontPage"))
    else:
        post = blogPosts.getPost(postId)
        return render_template(
            "read.html",
            editable = postId,
            title = post.title,
            auth = post.auth,
            content = post.content,
            date = post.date)

@post.route("/edit/id=<postId>", methods = ["Get", "Post"])
def edit(postId):
    post = blogPosts.getPost(postId)
    if request.method == "POST":
        editPost(postId)
        return redirect("/post/read/id={}".format(postId))
    return render_template(
        "edit.html",
        auth = post.auth,
        title = post.title,
        current = post.content,
        date = post.date)

def createNewPost():
    author = request.form.get("author")
    title = request.form.get("title")
    content = request.form.get("post")
    blogPosts.addPost(Post(author, title, content))    


def editPost(id):
    author = request.form.get("author")
    title = request.form.get("title")
    content = request.form.get("post")
    editted = Post(author, title, content)
    blogPosts.replace(id, editted)    