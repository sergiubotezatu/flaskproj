from unittest import mock
from services.posts_db_repo import PostsDb
from services.posts_in_memo import Posts
from services import ipost_repo, idata_base
from services.database import DataBase


class Container:
    def __init__(self):
        self.prod_services = {ipost_repo.IPostRepo : PostsDb(), idata_base.IDataBase : DataBase()}
        self.test_services = {ipost_repo.IPostRepo : Posts(), idata_base.IDataBase: None}

    def get(self, is_test : bool) -> dict:
        return self.test_services if is_test else self.prod_services
