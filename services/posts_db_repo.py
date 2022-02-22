from psycopg2 import connect, DatabaseError
from services.ipost_repo import IPostRepo
from models.post import Post
from services.database import DataBase

class PostsDb(IPostRepo):
    def __init__(self):
        self.count = 0
        self.db = DataBase()
        self.table = self.edit_table("creation")

    def __len__(self):
        return self.count
    
    def add_post(self, post):
        self.edit_table(
            "insertion",
            self.create_id(post.auth),
            post.auth, post.title,
            post.content,
            post.date)

    def replace(self, post, id):
        self.edit_table("edit", post.auth, post.title, post.content, post.date, id)

    def remove(self, id):
        self.edit_table("deletion", id)
    
    def create_id(self, name):
        return name[:2] + str(self.count + 1)

    def get_post(self, id):
        self.read(id)

    def get_all(self):
        self.read()
    
    def edit_table(self, request, *args):
        execution = self.get_all_options()[request]
        try:
            conn = self.db.connection()
            cursor = conn.cursor()
            cursor.execute(execution, args)
            conn.commit()
            cursor.close()
        except (Exception, DatabaseError) as error:
            print(error)
        conn.close()

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
            PostID SERIAL PRIMARY KEY,
            Author varchar(30),
            Title varchar(200),
            Content varchar(3000),
            Date varchar(20)
        );
        """
    
    def insertion(self):
        return """
            INSERT INTO blog_posts       
            VALUES (%s, %s, %s, %s, %s);
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
    
    def read(self, id = ""):
        result = None
        try:
            conn = self.db_connect()
            cursor = conn.cursor()
            if id == "":
                cursor.execute(self.read_all(), "Content")
                result = []
                row = cursor.fetchone()
                while row is not None:
                    result.append(row[0], row[1], row[2], self.fit_newlines(row[3]), row[4])
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

    def read_all(self, cursor):
        return"""
            SELECT SUBSTRING(%s, 1, 150)
            FROM blog_posts;
            """

    def fit_newlines(self, content):
        lines_count = content.count("\n")
        if lines_count > 0:
            chunk = lines_count * 3
            return content[:-chunk] + "[...]"
        return content + "[...]"