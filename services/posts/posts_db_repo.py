from psycopg2 import DatabaseError
from services.interfaces.ipost_repo import IPostRepo
from services.interfaces.idata_base import IDataBase
from models.post import Post
from services.dependency_inject.injector import Services
from services.database.repos_queries import queries, fetch_if_needed

class PostsDb(IPostRepo):
    @Services.get
    def __init__(self, db : IDataBase):
        self.__count = -1
        self.db = db
        
    @property
    def count(self):
        if self.__count == -1:
            return self.db.perform("count_posts")[0]
        return self.__count

    @count.setter
    def count(self, value):
        self.__count = value
                
    def __len__(self):
        return self.count
    
    def add_post(self, post : Post):
        self.count += 1
        return self.db.perform("insert_post", post.title, post.content, post.created, post.owner_id)[0]     

    def replace(self, id, post : Post):
        self.db.perform("edit_post", post.title, post.content, post.created, id)

    def remove(self, id):
        self.count -= 1
        self.db.perform("delete_post", id)   
    
    def get_post(self, id) -> Post:
        displayed = self.db.perform("read_post", id)
        post = Post(displayed[0], displayed[1], displayed[2], owner_id = displayed[3], date = displayed[4])
        post.modified = displayed[5]
        return post

    def get_all(self):
        return self.__get_fetched(self.db.perform("read_all"))

    def __get_fetched(self, fetched):
        result = []
        for post in fetched:
            result.append((post[0], Post(post[1], post[2], post[3], owner_id= post[4], date = post[5])))
        return result
