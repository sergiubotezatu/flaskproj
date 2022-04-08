from flask import Blueprint, render_template, request, url_for, redirect
from models.db_settings import DBSettings
from services.database.config import Config
from services.database.database import DataBase
from services.interfaces.Ipassword_hash import IPassHash
from services.interfaces.idata_base import IDataBase
from services.dependency_inject.injector import Services
from datetime import datetime

from services.interfaces.idb_upgrade import IDataBaseUpgrade

class DbSetUp:
    @Services.get
    def __init__(self, db : IDataBase, hasher : IPassHash):
        self.database = db
        self.config = Config()
        self.hasher = hasher
        self.upgrader : IDataBaseUpgrade = self.database.upgrader
        self.bp = Blueprint("db_setup", __name__)
        self.db_settings = self.bp.route("/config", methods = ["Get", "Post"])(self.set_database)
        self.upgrade_if_older()
        
    def set_database(self):
        if self.database.config.is_configured:
            return redirect(url_for("home.front_page"))
        if request.method == "POST":
            settings = DBSettings(self.get_items())        
            self.database.config.save(settings)
            self.upgrade_if_older()
            return redirect(url_for("home.front_page"))
        return render_template("db_setup.html")
    
    def get_items(self):
        return [
            "postgresql",
            request.form.get("database"),
            request.form.get("user"),
            request.form.get("password"),
            request.form.get("host")
        ]

    def upgrade_if_older(self):
        if self.database.config.section_exists("postgresql"):
            self.database.set_db()
        if not self.upgrader.is_latest_version():
            admin_pass = self.hasher.generate_pass('admin1')
            dummy_pass = self.hasher.generate_pass('dummy')
            admin_creation = datetime.now().strftime("%d/%b/%y %H:%M:%S")   
            self.database.upgrade_db(admin_pass, admin_creation, dummy_pass)
