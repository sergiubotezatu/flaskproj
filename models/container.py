from services.posts_db_repo import PostsDb
from services.posts_in_memo import Posts
from services.ipost_repo import IPostRepo
from services.database import DataBase

class Container:
    def __init__(self):
        self.prod_services = {IPostRepo : PostsDb()}
        self.test_services = {IPostRepo : Posts(), "IDataBase" : DataBase}

    def get(self, is_test : bool) -> dict:
        return self.test_services if is_test else self.prod_services
