from configparser import ConfigParser 
from psycopg2 import connect, DatabaseError
from services.database_config import DataBaseConfig

class DataBase:
    def __init__(self):
        self.config = DataBaseConfig()
        self.conn = None
        self.cursor = None

    def connection(self):
        return connect(self.config.current_config)    

    def create_database(self):
        try:
            self.db_connect()
            self.cursor.execute(self.table_creation())
            got_id = self.cursor.fetchone()
            id = got_id[0] if got_id != None else id
            self.commit_and_close()
        except (Exception, DatabaseError) as error:
            print(error)

    def db_connect(self):
        self.conn = self.connection
        self.cursor = self.conn.cursor()

    def commit_and_close(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
    
    def table_creation(self):
        return """        
            CREATE TABLE IF NOT EXISTS blog_posts(
            PostID SERIAL PRIMARY KEY,
            Author varchar(30),
            Title varchar(200),
            Content varchar(3000),
            Date varchar(20));        
        """
