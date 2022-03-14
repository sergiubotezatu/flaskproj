from resources.posts_db_repo import PostsDb
from resources.posts_in_memo import Posts
from resources.database import DataBase
from resources.idata_base import IDataBase
from resources.ipost_repo import IPostRepo
from resources.idatabase_config import IDataBaseConfig
from resources.database_config import DataBaseConfig
from resources.mock_db_config import MockDbConfig

class Container:
    DEPENDENCIES = {
        IPostRepo : IDataBase,
        IDataBase : IDataBaseConfig,
        IDataBaseConfig : None,
        Posts : None}

    prod_services = {
        IPostRepo : PostsDb,
        IDataBase : DataBase,
        IDataBaseConfig : DataBaseConfig}

    test_services = {
        IPostRepo : Posts,
        IDataBase: DataBase,
        IDataBaseConfig: MockDbConfig.mocked_db_config}

    def __init__(self, is_test):
        self.items = self.get(is_test)
    
    def get(self, is_test : bool) -> dict:
        return self.test_services if is_test else self.prod_services
   