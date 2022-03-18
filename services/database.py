import psycopg2
from services.idata_base import IDataBase
from services.idatabase_config import IDataBaseConfig
from services.resources import Services

class DataBase(IDataBase):
    config = None

    @Services.get
    def __init__(self, config : IDataBaseConfig):
        DataBase.config = config
        self.conn = None
        self.cursor = None
    
    @classmethod
    def initialize_db(cls, settings):
        cls.config.add_settings(settings)
        cls.config.save()
        cls.config.load()

    def create_database(self):
        try:
            self.connect()
            for operation in self.table_creation():
                self.cursor.execute(operation)
            self.commit_and_close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def connect(self):
        self.conn = psycopg2.connect(**self.config.current_config)
        self.cursor = self.conn.cursor()

    def commit_and_close(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
    
    def table_creation(self):
        return ("""      
            CREATE TABLE IF NOT EXISTS blog_users(
            OwnerID SERIAL PRIMARY KEY,
            Name varchar(30),
            Email varchar(200),
            Password varchar(5000),
            Date varchar(50),
            Date_modified varchar(50));
        """,
            """        
            CREATE TABLE IF NOT EXISTS blog_posts(
            PostID SERIAL PRIMARY KEY,
            Author varchar(30),
            Title varchar(200),
            Content varchar(5000),
            Date varchar(50),
            Date_modified varchar(50),
            OwnerID int,
            FOREIGN KEY (OwnerID) REFERENCES blog_users(OwnerID));
        """,
        """        
            CREATE TABLE IF NOT EXISTS deleted_users(
            Email varchar(200),
            Content varchar(5000));""")
