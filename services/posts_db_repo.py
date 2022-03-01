from psycopg2 import connect, DatabaseError
from services.ipost_repo import IPostRepo
from models.post import Post
from services.database import DataBase

class PostsDb(IPostRepo):
    def __init__(self):
        self.count = 0
        self.db = None

    def attach_db(self, db : DataBase):
        self.db = db
                
    def __len__(self):
        return self.count
    
    def add_post(self, post):
        self.count += 1
        return self.perform_query("insertion", post.auth, post.title, post.content, post.date)        

    def replace(self, post, id):
        self.perform_query("edit", post.auth, post.title, post.content, post.date, id)

    def remove(self, id):
        self.count -= 1
        self.perform_query("deletion", id)        
    
    def get_post(self, id):
        return self.read(id)

    def get_all(self):
        return self.read()    

    def perform_query(self, request, *args):
        id = -1
        execution = self.editing_queries()[request]
        try:
            self.db.db_connect()
            self.db.cursor.execute(execution, *args)
            got_id = self.db.cursor.fetchone()
            id = got_id[0] if got_id != None else id
            self.db.commit_and_close()
        except (Exception, DatabaseError) as error:
            print(error)
        return id

    def editing_queries(self):
        return {
        "insertion" : self.insertion,
        "edit" : self.update(),
        "deletion" : self.delete()
        }

    def read(self, id = ""):
        result = None
        try:
            self.db.db_connect()
            if id == "":
                result = []
                result.append(self.fetch_to_display(self.db.cursor, self.read_all()))
            else:
                result = self.fetch_to_display(self.db.cursor, self.read_post(id))
            self.db.commit_and_close()
        except (Exception, DatabaseError) as error:
            print(error)
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
            ELSE p.Content
            END AS Preview  
            FROM blog_posts AS p
            ORDER BY p.PostID DESC;
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

    def cut_poem_newlines(self, content):
        lines_count = content.count("\n")
        if lines_count > 0:
            chunk = lines_count * 3
            return content[:-chunk] + "[...]"
        return content + "[...]"
