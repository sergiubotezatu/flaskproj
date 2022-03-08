from psycopg2 import DatabaseError
from services.database import DataBase
from services.ipost_repo import IPostRepo
from services.idata_base import IDataBase
from models.post import Post
from services.services import Services

class PostsDb(IPostRepo):
    def __init__(self):
        self.__count = -1
        self.query = QueryPosts(IDataBase)
   
    @property
    def count(self):
        if self.__count == -1:
            return self.query.perform("count")
        return self.__count

    @count.setter
    def count(self, value):
        self.__count = value
                
    def __len__(self):
        return self.count
    
    def add_post(self, post : Post):
        self.count += 1
        return self.query.perform("insertion", post.auth, post.title, post.content, post.created)        

    def replace(self, id, post : Post):
        self.query.perform("edit", post.auth, post.title, post.content, post.created, id)

    def remove(self, id):
        self.count -= 1
        self.query.perform("deletion", id)   
    
    def get_post(self, id) -> Post:
        displayed = self.query.perform_read(id)
        post = Post(displayed[0], displayed[1], displayed[2], displayed[3])
        post.modified = displayed[4]
        return post

    def get_all(self):
        return self.query.perform_read()


class QueryPosts:
    @Services.get
    def __init__(self, db : IDataBase):
        self.db = db

    def attach(self, db):
        self.db = db
    
    def perform(self, request, *args):
        retrieved = 0
        execution = self.__queries()[request]
        try:
            self.db.connect()
            self.db.cursor.execute(execution, args)
            retrieved = self.__fetch_if_needed(request)
            self.db.commit_and_close()
        except (Exception, DatabaseError) as error:
            print(error)
        return retrieved
    
    def __queries(self):
        return {
        "insertion" : self.__insertion(),
        "edit" : self.__update(),
        "deletion" : self.__delete(),
        "count" : self.__count_rows()
        }
    
    def perform_read(self, id = "") -> Post:
        result = None
        try:
            self.db.connect()
            result = self.__fetch_all_posts(
                self.__read_all()) if id == "" else self.__fetch_post(self.__read_post(id))               
            self.db.commit_and_close()
        except (Exception, DatabaseError) as error:
            print(error)
        return result

    def __fetch_post(self, query):
        self.db.cursor.execute(query)
        return self.db.cursor.fetchone()        

    def __fetch_all_posts(self, query):
        self.db.cursor.execute(query)
        nextPost = self.db.cursor.fetchone()
        result = []
        while nextPost is not None:
            result.append(
            (nextPost[0], 
            Post
            (
            nextPost[1],
            nextPost[2],
            self.__cut_poem_newlines(nextPost[6]),
            nextPost[4])
            )
            )
            nextPost = self.db.cursor.fetchone()
        return result

    def __read_post(self, id):
        return f"""
                SELECT Author, Title, Content, Date, Date_modified
                FROM blog_posts
                WHERE PostID = {id};
            """

    def __read_all(self):
        return"""
            SELECT p.*,
            CASE
            WHEN CHAR_LENGTH(p.Content) > 150 THEN SUBSTRING(p.Content, 1, 150)
            ELSE p.Content
            END AS Preview  
            FROM blog_posts AS p
            ORDER BY p.PostID DESC;
            """

    def __insertion(self):
        return """
        INSERT INTO blog_posts       
        VALUES (DEFAULT, %s, %s, %s, %s)
        RETURNING PostID;
        """

    def __update(self):
        return """
            UPDATE blog_posts
            SET Author = %s, Title= %s, Content = %s, Date_modified = %s
            WHERE PostID = %s;
        """

    def __delete(self):
        return """
            DELETE FROM blog_posts
            WHERE PostID = %s;
            """

    def __count_rows(self):
        return """
            SELECT
            COUNT(Content)
            FROM blog_posts;
            """

    def __cut_poem_newlines(self, content):
        lines_count = content.count("\n")
        if lines_count > 0:
            chunk = lines_count * 3
            return content[:-chunk] + "[...]"
        return content + "[...]"

    def __fetch_if_needed(self, request):
        if request == "insertion" or request == "count":
            return self.db.cursor.fetchone()[0]
        return 0