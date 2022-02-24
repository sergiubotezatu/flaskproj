from psycopg2 import connect, DatabaseError
from services.ipost_repo import IPostRepo
from models.post import Post
from services.database import DataBase

class PostsDb(IPostRepo):
    def __init__(self):
        self.count = 0
        self.db = DataBase()
                
    def __len__(self):
        return self.count
    
    def add_post(self, post):
        self.count += 1
        return self.db.perform_query("insertion", post.auth, post.title, post.content, post.date)        

    def replace(self, post, id):
        self.db.perform_query("edit", post.auth, post.title, post.content, post.date, id)

    def remove(self, id):
        self.db.perform_query("deletion", id)
        self.count -= 1
    
    def get_post(self, id):
        self.read(id)

    def get_all(self):
        self.read()

    def read(self, id = ""):
        result = None
        try:
            conn = self.db.connection()
            cursor = conn.cursor()
            if id == "":
                result = []
                result.append(self.fetch_to_display(cursor, self.read_all))
            else:
                result = self.fetch_to_display(cursor, self.read_post(id))
            conn.close()
            cursor.close()
        except (Exception, DatabaseError) as error:
            print(error)
        conn.close()
        return result

    def fetch_to_display(self, cursor, func_read):
        cursor.execute(func_read)
        row = cursor.fetchone()
        while row is not None:
            yield Post(row[0], row[1], row[2], self.cut_poem_newlines(row[5]), row[4])
            row = cursor.fetchone()

    def read_post(self, id):
        return f"""
                SELECT * FROM blog_posts
                WHERE PostID = {id};
            """

    def read_all(self):
        return"""
            SELECT p.*,
            CASE
            WHEN CHAR_LENGTH(p.Content) > 150 THEN SUBSTRING(p.Content, 1, 150)
            ELSE C.Content
            END AS Preview  
            FROM blog_posts AS p
            ORDER BY p.PostID DESC;
            """

    def cut_poem_newlines(self, content):
        lines_count = content.count("\n")
        if lines_count > 0:
            chunk = lines_count * 3
            return content[:-chunk] + "[...]"
        return content + "[...]"
