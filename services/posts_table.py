from psycopg2 import connect, DatabaseError
from services.data_source import ISource

class PostsTable(ISource):
    def __init__(self):
        self.conn = None
        self.register_table()
        self.count = 0

    def __len__(self):
        return self.count
    
    def init_connect(self):
        return connect(
            host = "localhost",
            database = "posts",
            user = "postgres",
            password = "sergiu"
        )

    def register_table(self):
        self.access_db(self.create_table())
    
    def add_post(self, post):
        self.access_db(self.insert_post(post))
        self.count += 1

    def replace(self, post, id):
        self.access_db(self.update_post(post, id))

    def remove(self, id):
        self.access_db(self.delete_post(id))

    def access_db(self, operation):
        try:
            self.conn = self.init_connect()
            cursor = self.conn.cursor()
            cursor.execute(operation)
            self.conn.commit()
            cursor.close()
        except (Exception, DatabaseError) as error:
            print(error)
        self.conn.close()
    
    def create_table(self):
          return """
                CREATE TABLE blog_posts (
                    PostId char(3),
                    Author varchar(30),
                    Title varchar(200),
                    Content varchar(3000),
                    Date varchar(20)
                )
                """
    def insert_post(self, post):
        return ("""
            INSERT INTO blog_posts       
            VALUES (%s, %s, %s, %s, %s)
            """, (self.create_id(post.auth), post.auth, post.title, post.content, post.date))

    def update_post(self, post, id):
        return """
            UPDATE blog_posts
            SET Author = %s, Title= %s, Content = %s, Date = %s
            WHERE PostID = %s;
        """, (post.auth, post.title, post.content, post.date, id)

    def delete_post(self, id):
         return """
            DELETE FROM blog_posts
            WHERE PostID = %s;
        """, (id)
    
    def create_id(self, name):
        return name[:2] + str(self.count + 1)
