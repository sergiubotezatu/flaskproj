from services.posts_db_repo import PostsDb
from services.posts_in_memo import Posts
from services.database import DataBase
from services.idata_base import IDataBase
from services.ipost_repo import IPostRepo
from services.idatabase_config import IDataBaseConfig
from services.database_config import DataBaseConfig
from services.iusers import IUsers
from services.users_in_memo import Users
from services.users_db_repo import UsersDb
from services.mock_db_config import MockDbConfig

class Container:
    DEPENDENCIES = {
        IPostRepo : IDataBase,
        IDataBase : IDataBaseConfig,
        IDataBaseConfig : None,
        Posts : None,
        IUsers : IDataBase}

    prod_services = {
        IPostRepo : PostsDb,
        IDataBase : DataBase,
        IDataBaseConfig : DataBaseConfig,
        IUsers : UsersDb
        }

    test_services = {
        IPostRepo : Posts,
        IDataBase: DataBase,
        IDataBaseConfig: MockDbConfig.mocked_db_config,
        IUsers : Users}

    def __init__(self, is_test):
        self.items = self.get(is_test)
    
    def get(self, is_test : bool) -> dict:
        return self.test_services if is_test else self.prod_services
   