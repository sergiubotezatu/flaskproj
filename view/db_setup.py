from flask import Blueprint, render_template, request, url_for, redirect

class DbSetUp:
    def __init__(self, db_repo):
        self.db_repo = db_repo
        self.bp = Blueprint("db_setup", __name__)
        self.db_settings = self.bp.route("/config", methods = ["Get", "Post"])(self.set_database)
    
    def set_database(self):
        if self.db_repo.db.current_config != None:
            return redirect(url_for("home.front_page"))             
        if request.method == "POST":
            self.db_repo.db.add_new_config(request.form.get("section"), self.get_items())
            return redirect(url_for("home.front_page"))
        return render_template("db_setup.html")             
    
    def get_items(self):
        return [
            request.form.get("host"),
            request.form.get("database"),
            request.form.get("user"),
            request.form.get("password")
        ]