import psycopg2
from services.idata_base import IDataBase
from services.idatabase_config import IDataBaseConfig
from services.idb_upgrade import IDataBaseUpgrade
from services.resources import Services
from services.repos_queries import queries, fetch_if_needed

class DataBase(IDataBase):
    config = None

    @Services.get
    def __init__(self, config : IDataBaseConfig, upgrader : IDataBaseUpgrade):
        DataBase.config = config
        self.conn = None
        self.cursor = None
        self.upgrader = upgrader    
    
    def connect(self):
        self.conn = psycopg2.connect(**self.config.current_config)
        self.cursor = self.conn.cursor()

    def commit_and_close(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    @classmethod
    def initialize_db(cls, settings):
        cls.config.add_settings(settings)
        cls.config.save()
        cls.config.load()

    def upgrade_db(self, *args):
        if not self.upgrader.is_latest_version():
            try:
                self.connect()
                for operation in self.upgrader.upgrade():
                    self.cursor.execute(operation, args)
                self.commit_and_close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)


    def perform(self, request, *args):
        retrieved = 0
        execution = queries()[request]
        try:
            self.connect()
            self.cursor.execute(execution, args)
            retrieved = fetch_if_needed(request, self.cursor)
            self.commit_and_close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        return retrieved   
   