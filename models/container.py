from unittest import mock
from resources.posts_db_repo import PostsDb
from resources.posts_in_memo import Posts
from resources.database import DataBase
from resources.idata_base import IDataBase
from resources.ipost_repo import IPostRepo
from resources.idatabase_config import IDataBaseConfig
from resources.database_config import DataBaseConfig

class Container:
    DEPENDENCIES = {
        IPostRepo : IDataBase,
        IDataBase : IDataBaseConfig,
        IDataBaseConfig : None,
        Posts : None}
    def __init__(self,):
        self.prod_services = {
            IPostRepo : PostsDb,
            IDataBase : DataBase,
            IDataBaseConfig : DataBaseConfig}

        self.test_services = {
            IPostRepo : Posts,
            IDataBase: self.mocked_dataBase,
            IDataBaseConfig: self.mocked_db_config}
        
    def get(self, is_test : bool) -> dict:
        return self.test_services if is_test else self.prod_services

    def mocked_dataBase(self):
        mock_db = mock.create_autospec(DataBase)
        return mock_db

    def mocked_db_config(self):
        mock_config = mock.create_autospec(DataBaseConfig)
        return mock_config

