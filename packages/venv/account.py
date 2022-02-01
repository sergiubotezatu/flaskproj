from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from user import User
from registered import Registered
from post import Post
from posts import allPosts

profile = Blueprint("profile", __name__)

allAccounts = Registered()

@profile.route("/log_in", methods = ["Get", "Post"])
def log():
     if request.method == "POST":
         username = request.form.get("username")
         password = request.form.get("pwd")
         if not allAccounts.searchUser(username):
              flash(("Username {} is not assigned to any registered members\nCheck for spelling errors"
              "Click on \"Here\" below the form if you don't have an account".format(username)), "error")
              return redirect(url_for(".log"))

         elif not allAccounts.getUserByName(username).checkPass(password):
              flash("Incorrect Password. Please try again", "error")
              return redirect(url_for(".log"))

         session.permanent = True
         session["profile"] = username
         return redirect(url_for(".userProfile", name = str(username)))              

     return render_template("login.html")

@profile.route("/sign_up", methods = ["GET", "POST"])
def sign():
    if request.method == "POST":
         username = request.form.get("username")
         password = request.form.get("pwd")
         if createAccount(User(username, password)):
               session["profile"] = username
               flash(("Welcome, {}!\n/This is your profile page. Here you can see all of your posts "
               "Click on [Create Post] button to add a new post".format(username)), "info")
               return redirect(url_for(".userProfile", name = str(username)))
         else:
               flash(("Username {} is already assigned to another user. "
               "Please use a different userName".format(username)), "error")
               return redirect(url_for(".sign"))
    
    return render_template("signUp.html")

@profile.route("/log_out")
def logOut():
     session.pop("profile", None)
     return redirect(url_for("posts.home"))

@profile.route("/user=<name>")
def userProfile(name):
     if "profile" in session:
          return render_template("user.html", user="{}'s profile".format(session["profile"]))
     else:
          return redirect(url_for(".log"))

@profile.route("/create", methods = ["Get", "Post"])
def createPost():
     if request.method == "POST":
         registerPost()
         return redirect(url_for("posts.home"))
     return render_template("write.html")

def createAccount(newUser):
     if allAccounts.searchUser(newUser.userName):
          return False
     else:
          allAccounts.register(newUser)
          return True

def registerPost():
     title = request.form.get("title")
     description = request.form.get("description")
     content = request.form.get("post")
     author = session["profile"]
     post = Post(title, description, content, author)
     allAccounts.getUserByName(session["profile"]).addPost(post)
     allPosts.insert(0, post)
     