from configparser import ConfigParser, DatabaseError
from psycopg2 import connect
from models.post import Preview, Post

class PostsDbWork:
    def __init__(self, request):
        self.request = request
        self.generate_table = self.edit_table(request)

    def edit_table(self, *args):
        execution = self.get_all_options()[self.request]
        try:
            conn = self.db_connect()
            cursor = conn.cursor()
            cursor.execute(execution, args)
            conn.commit()
            cursor.close()
        except (Exception, DatabaseError) as error:
            print(error)
        self.conn.close()

    def db_connect(self):
        configuration = self.config()
        return connect(configuration)  

    def config(filename='database.ini', section='postgresql'):
        parser = ConfigParser() 
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception(f"Section {section} not found in the {filename} file")

        return db      

    def get_all_options(self):
        return {
        "creation" : self.table_creation(),
        "insertion" : self.insertion,
        "edit" : self.update(),
        "deletion" : self.delete()
        }

    def table_creation(self):
        return """        
            CREATE TABLE [IF NOT EXISTS] blog_posts (
            PostId char(3),
            Author varchar(30),
            Title varchar(200),
            Content varchar(3000),
            Date varchar(20)
        )
        """

    def insertion(self):
        return """
            INSERT INTO blog_posts       
            VALUES (%s, %s, %s, %s, %s)
            """

    def update(self):
        return """
            UPDATE blog_posts
            SET Author = %s, Title= %s, Content = %s, Date = %s
            WHERE PostID = %s;
        """

    def delete(seld):
        return """
            DELETE FROM blog_posts
            WHERE PostID = %s;
            """
    
    def read(self, id = ""):
        result = None
        try:
            conn = self.db_connect()
            cursor = conn.cursor()
            if id == "":
                cursor.execute(self.get_all())
                result = []
                row = cursor.fetchone()
                while row is not None:
                    result.append(row[0], Preview(row[1], row[2], row[3], row[4]))
            else:
                cursor.execute(self.read_post())
                row = cursor.fetchone()
                result = Post(row[1], row[2], row[3], row[4])
            cursor.close()
        except (Exception, DatabaseError) as error:
            print(error)
        conn.close()
        return result

    def read_post(self, cursor):
        return"""
                SELECT * FROM blog_posts
                WHERE PostID = %s;
            """

    def get_all(self, cursor):
        return"""
            SELECT * FROM blog_posts
            """
