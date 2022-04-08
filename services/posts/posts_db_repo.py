from psycopg2 import DatabaseError
from services.interfaces.ipost_repo import IPostRepo
from services.interfaces.idata_base import IDataBase
from models.post import Post
from services.dependency_inject.injector import Services

class PostsDb(IPostRepo):
    @Services.get
    def __init__(self, db : IDataBase):
        self.__count = -1
        self.db = db
        
    @property
    def count(self):
        if self.__count == -1:
            return self.db.perform("""
            SELECT
            COUNT(Content)
            FROM blog_posts;
            """, fetch = "fetchone")[0]
        return self.__count

    @count.setter
    def count(self, value):
        self.__count = value
                
    def __len__(self):
        return self.count
    
    def add_post(self, post : Post):
        self.count += 1
        return self.db.perform("""
        INSERT INTO blog_posts (PostID, Title, Content, Date, OwnerID)     
        VALUES (DEFAULT, %s, %s, %s, %s)
        RETURNING PostID;
        """, post.title, post.content, post.created, post.owner_id, fetch = "fetchone")[0]     

    def replace(self, id, post : Post):
        self.db.perform("""
            UPDATE blog_posts
            SET Title= %s, Content = %s, Date_modified = %s
            WHERE PostID = %s;
        """, post.title, post.content, post.created, id)

    def remove(self, id):
        self.count -= 1
        self.db.perform("""
            DELETE FROM blog_posts
            WHERE PostID = %s;
            """, id)   
    
    def get_post(self, id) -> Post:
        displayed = self.db.perform("""
           SELECT
                u.Name,
                p.title,
                p.content,
                u.OwnerID,
                p.date,
                p.Date_modified
            FROM
                blog_users u
            INNER JOIN blog_posts p
                ON u.OwnerID = p.OwnerID
                where p.PostID = %s;
            """, id, fetch = "fetchone")
        post = Post(displayed[0], displayed[1], displayed[2], owner_id = displayed[3], date = displayed[4])
        post.modified = displayed[5]
        return post

    def get_all(self):
        return self.__get_fetched(self.db.perform("""
            SELECT p.PostID,
            u.Name,
            p.Title,
            SUBSTRING(p.Content, 1, 150),
            p.OwnerID,
            p.Date
            FROM blog_posts p
            INNER JOIN blog_users u
            ON p.OwnerID = u.OwnerID 
            ORDER BY p.PostID DESC;
            """, fetch = "fetchall"))

    def unarchive_content(self, id, name, email):
        result = self.db.perform("""
        SELECT Content
        FROM deleted_users
        WHERE Email = %s;
        """, email, fetch = "fetchall")
        i = 1
        for record in result:
            self.add_post(Post(name, f"post no {i}", record[0], owner_id = id))
            i += 1
        self.db.perform("""
        DELETE FROM deleted_users
        WHERE Email = %s;
        """, email)

    def __get_fetched(self, fetched):
        result = []
        for post in fetched:
            result.append((post[0], Post(post[1], post[2], post[3], owner_id= post[4], date = post[5])))
        return result
