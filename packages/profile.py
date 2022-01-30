from flask import Blueprint, render_template, request, redirect, url_for, flash
from packages.user import User
from packages.registered import Registered

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

         return redirect(url_for(".userProfile", name = str(username)))              

     return render_template("login.html")

@profile.route("/sign_up", methods = ["GET", "POST"])
def sign():
    if request.method == "POST":
         username = request.form.get("username")
         password = request.form.get("pwd")
         if createAccount(User(username, password)):
               flash(("Welcome, {}!\n/This is your profile page. Here you can see all of your posts "
               "Click on [Create Post] button to add a new post".format(username)), "info")
               return redirect(url_for(".userProfile", name = str(username)))
         else:
               flash(("Username {} is already assigned to another user. "
               "Please use a different userName".format(username)), "error")
               return redirect(url_for(".sign"))
    
    return render_template("signUp.html")

@profile.route("/user=<name>")
def userProfile(name):
     return render_template("user.html", user="{}'s profile".format(name))


def createAccount(newUser):
     if allAccounts.searchUser(newUser.userName):
          return False
     else:
          allAccounts.register(newUser)
          return True
