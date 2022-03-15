from flask import Blueprint, render_template, request, url_for, redirect
from models.db_settings import DBSettings
from services.idata_base import IDataBase
from services.resources import Services

class DbSetUp:
    @Services.get
    def __init__(self, db : IDataBase):
        self.database = db
        self.bp = Blueprint("db_setup", __name__)
        self.db_settings = self.bp.route("/config", methods = ["Get", "Post"])(self.set_database)
    
    def set_database(self):
        if self.database.config.is_configured:
            return redirect(url_for("home.front_page"))             
        if request.method == "POST":
            settings = DBSettings(self.get_items())        
            self.database.initialize_db(settings)
            self.database.create_database()
            return redirect(url_for("home.front_page"))
        return render_template("db_setup.html")             
    
    def get_items(self):
        return [
            request.form.get("host"),
            request.form.get("database"),
            request.form.get("user"),
            request.form.get("password")
        ]