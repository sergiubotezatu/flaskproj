from psycopg2 import connect, DatabaseError
from services.ipost_repo import IPostRepo
from models.post import Post
from services.posts_db_actions import PostsDbWork

class PostsDb(IPostRepo):
    def __init__(self):
        self.table = PostsDbWork("creation")
        self.count = 0

    def __len__(self):
        return self.count
    
    def add_post(self, post):
        self.table.edit_table(
            "insertion",
            self.create_id(post.auth),
            post.auth, post.title,
            post.content,
            post.date)

    def replace(self, post, id):
        self.table.edit_table("edit", post.auth, post.title, post.content, post.date, id)

    def remove(self, id):
        self.table.edit_table("deletion", id)
    
    def create_id(self, name):
        return name[:2] + str(self.count + 1)

    def get_post(self, id):
        self.table.read(id)

    def get_preview(self):
        self.table.read()
