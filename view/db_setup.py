from flask import Blueprint, render_template, request, url_for, redirect
from models.db_settings import DBSettings
from services.database.config import Config
from services.database.sqlalchemy import SqlAlchemy
from services.interfaces.idata_base import IDataBase
from services.dependency_inject.injector import Services
from services.interfaces.idb_upgrade import IDataBaseUpgrade

class DbSetUp:
    @Services.get
    def __init__(self, db : IDataBase, with_alchemy : bool):
        self.database = db
        self.config = Config()
        self.upgrader : IDataBaseUpgrade = self.database.upgrader
        self.bp = Blueprint("db_setup", __name__)
        self.db_settings = self.bp.route("/config", methods = ["Get", "Post"])(self.set_database)
        self.upgrade_if_older(with_alchemy)
        
    def set_database(self):
        if self.database.config.is_configured:
            return redirect(url_for("home.front_page"))
        if request.method == "POST":
            settings = DBSettings("postgresql",
                        request.form.get("database"),
                        request.form.get("user"),
                        request.form.get("password"),
                        request.form.get("host"))
            self.database.config.save(settings)
            self.upgrade_if_older()
            return redirect(url_for("home.front_page"))
        return render_template("db_setup.html")

    def upgrade_if_older(self, with_alchemy = False):
        if self.database.config.section_exists("postgresql"):
            self.database.set_db()
            self.config_sqlalchemy(with_alchemy)
            if not self.upgrader.is_latest_version():
                self.database.upgrade_db()

    def config_sqlalchemy(self, with_alchemy):
        if with_alchemy:
            settings = self.database.config.load()
            SqlAlchemy.configure(settings)

