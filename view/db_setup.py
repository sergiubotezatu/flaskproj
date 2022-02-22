from flask import Blueprint, render_template, request, url_for, redirect

class DbSetUp:
    def __init__(self, db_repo):
        self.db_repo = db_repo
        self.bp = self.create_bp()

    def create_bp(self):
        db_setup = Blueprint("db_setup", __name__)

        @db_setup.route("/db_config", methods = ["Get", "Post"])
        def set_database():
            if request.method == "POST":
                self.db_repo.add_new_config(self.get_items(), request.form.get("section"))
                return redirect(url_for("home.front_page"))
            return render_template("db_setup.html")        

        return db_setup

    def get_items(self):
        items = [
            request.form.get("host"),
            request.form.get("database"),
            request.form.get("user"),
            request.form.get("password")
        ]