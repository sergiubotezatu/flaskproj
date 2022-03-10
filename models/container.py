from unittest import mock
from services.posts_db_repo import PostsDb
from services.posts_in_memo import Posts
from services.idata_base import IDataBase
from services.ipost_repo import IPostRepo
from services.database import DataBase
import services


class Container:
    def __init__(self,):
        self.prod_services = {IDataBase : DataBase, IPostRepo : PostsDb}
        self.test_services = {IDataBase: self.mocked_dataBase, IPostRepo : Posts}
                
    def get(self, is_test : bool) -> dict:
        return self.test_services if is_test else self.prod_services

    def mocked_dataBase(self):
        mock_db = mock.create_autospec(DataBase)
        return mock_db

