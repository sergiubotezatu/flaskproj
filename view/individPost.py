from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.collection import blogPosts
from models.post import Post

post = Blueprint("posts", __name__)

@post.route("/create", methods = ["Get", "Post"])
def create():
    if request.method == "POST":
        createNewPost()
        return redirect("/post/read/id={}".format(blogPosts.getIds()[-1]))

    return render_template("writePost.html")

@post.route("/read/id=<postId>")
def read(postId):
    post = blogPosts.getPost(postId)
    return render_template("read.html",title = post.title, author = post.auth, content = post.content)

@post.route("/edit")
def edit():
    return render_template("home.html")

@post.route("")
def RouteId(postId):
    return render_template("writePost.html")

def createNewPost():
    author = request.form.get("author")
    temp = request.form.get("title")
    title = "" if temp == "no title..." else temp
    content = request.form.get("post")
    blogPosts.addPost(Post(author, title, content))