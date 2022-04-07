import psycopg2
from models.db_settings import DBSettings
from services.interfaces.idata_base import IDataBase
from services.interfaces.idatabase_config import IDataBaseConfig
from services.interfaces.idb_upgrade import IDataBaseUpgrade
from services.dependency_inject.injector import Services

class DataBase(IDataBase):
    config = None
    db_settings = DBSettings

    @Services.get
    def __init__(self, config : IDataBaseConfig, upgrader : IDataBaseUpgrade):
        DataBase.config = config
        self.upgrader = upgrader
        self.conn = None
        self.cursor = None
    
    def connect(self):
        self.conn = psycopg2.connect(**DataBase.db_settings.configuration)
        self.cursor = self.conn.cursor()

    def commit_and_close(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def upgrade_db(self, *args):
        if not self.upgrader.is_latest_version():
            try:
                self.connect()
                for operation in self.upgrader.upgrade():
                    self.cursor.execute(operation, args)
                self.commit_and_close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)

    def perform(self, query, *args, fetch = ""):
        retrieved = None
        try:
            self.connect()
            self.cursor.execute(query, args)
            if fetch != "":
                retrieved = getattr(self.cursor, fetch)()
            self.commit_and_close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        return retrieved

    @classmethod
    def set_db(cls):
        cls.db_settings = cls.config.load("postgresql")
   