from flask import Blueprint, render_template, request, url_for, redirect
from services.posts_db_repo import PostsDb

db_setup = Blueprint("db_setup", __name__)

@db_setup.route("/config<repo>", methods = ["Get", "Post"])
def set_database(repo):
    db_repo = request.args.get(repo, type = PostsDb)
    if db_repo.db.current_config != None:
        return redirect(url_for(url_for("home.front_page")))
    if request.method == "POST":
        db_repo.db.add_new_config(get_items(), request.form.get("section"))
        return redirect(url_for("home.front_page"))
    return render_template("db_setup.html")

def get_items():
    items = [
        request.form.get("host"),
        request.form.get("database"),
        request.form.get("user"),
        request.form.get("password")
    ]