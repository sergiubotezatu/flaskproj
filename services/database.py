from configparser import ConfigParser 
from psycopg2 import connect, DatabaseError
from services.database_config import DataBaseConfig
from models.post import Post

class DataBase:
    def __init__(self):
        self.config = DataBaseConfig()
        self.current_config = None

    def connection(self):
        return connect(self.current_config)

    def add_new_config(self, section, settings):
        self.config.save_config(section, settings)
        self.current_config = self.config.load_config(section)
        self.perform_query("creation")

    def perform_query(self, request, *args):
        id = -1
        execution = self.edit_queries()[request]
        try:
            conn = self.connection()
            cursor = conn.cursor()
            cursor.execute(execution, *args)
            got_id = cursor.fetchone()
            id = got_id[0] if got_id != None else id
            conn.commit()
            cursor.close()
            conn.close()
        except (Exception, DatabaseError) as error:
            print(error)
        return id

    def edit_queries(self):
        return {
        "creation" : self.table_creation(),
        "insertion" : self.insertion,
        "edit" : self.update(),
        "deletion" : self.delete()
        }

    def table_creation(self):
        return """        
            CREATE TABLE IF NOT EXISTS blog_posts(
            PostID SERIAL PRIMARY KEY,
            Author varchar(30),
            Title varchar(200),
            Content varchar(3000),
            Date varchar(20));        
        """
    
    def insertion(self):
        return """
            INSERT INTO blog_posts       
            VALUES (%s, %s, %s, %s)
            RETURNING PostID;
            """

    def update(self):
        return """
            UPDATE blog_posts
            SET Author = %s, Title= %s, Content = %s, Date = %s
            WHERE PostID = %s;
        """

    def delete(self):
        return """
            DELETE FROM blog_posts
            WHERE PostID = %s;
            """