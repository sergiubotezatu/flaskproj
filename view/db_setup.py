from flask import Blueprint, render_template, request, url_for, redirect
from models.db_settings import DBSettings
from services.interfaces.Ipassword_hash import IPassHash
from services.interfaces.idata_base import IDataBase
from services.dependency_inject.injector import Services
from datetime import datetime

from services.interfaces.idb_upgrade import IDataBaseUpgrade

class DbSetUp:
    @Services.get
    def __init__(self, db : IDataBase, hasher : IPassHash):
        self.database = db
        self.hasher = hasher
        self.upgrader : IDataBaseUpgrade = self.database.upgrader
        self.bp = Blueprint("db_setup", __name__)
        self.db_settings = self.bp.route("/config", methods = ["Get", "Post"])(self.set_database)
        self.upgrade_if_older()
        
    def set_database(self):
        if request.method == "POST":
            settings = DBSettings(self.get_items())        
            self.database.initialize_db(settings)
        elif not self.database.config.is_configured:
            return render_template("db_setup.html")       
        admin_pass = self.hasher.generate_pass('admin1')
        admin_creation = datetime.now().strftime("%d/%b/%y %H:%M:%S")   
        self.database.upgrade_db(admin_pass, admin_creation)
        return redirect(url_for("home.front_page"))
                  
    
    def get_items(self):
        return [
            request.form.get("host"),
            request.form.get("database"),
            request.form.get("user"),
            request.form.get("password")
        ]

    def upgrade_if_older(self):
        if self.database.config.is_configured and not self.upgrader.is_latest_version():
            self.database.upgrade_db()