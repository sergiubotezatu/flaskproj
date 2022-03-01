from flask import Blueprint, render_template, request, url_for, redirect
from services.ipost_repo import IPostRepo
from models.db_settings import DBSettings
from services.database import DataBase
from services.database_config import DataBaseConfig

class DbSetUp:
    def __init__(self, db_repo : IPostRepo):
        self.database = DataBase()
        self.db_repo = db_repo
        self.bp = Blueprint("db_setup", __name__)
        self.db_settings = self.bp.route("/config", methods = ["Get", "Post"])(self.set_database)
    
    def set_database(self):
        if self.database.config.current_config != None:
            return redirect(url_for("home.front_page"))             
        if request.method == "POST":            
            self.database.config.add_settings(self.get_items())
            self.database.config.save()
            self.database.config.load()
            self.database.create_database()
            self.db_repo.attach_db(self.database)
            return redirect(url_for("home.front_page"))
        return render_template("db_setup.html")             
    
    def get_items(self):
        return [
            request.form.get("section"),
            request.form.get("host"),
            request.form.get("database"),
            request.form.get("user"),
            request.form.get("password")
        ]