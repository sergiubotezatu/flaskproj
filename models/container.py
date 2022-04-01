from services.Ipassword_hash import IPassHash
from services.db_upgrade import DataBaseUpgrade
from services.iauthentication import IAuthentication
from services.authentication import Authentication
from services.idb_upgrade import IDataBaseUpgrade
from services.passhash import PassHash
from services.posts_db_repo import PostsDb
from services.posts_in_memo import Posts
from services.database import DataBase
from services.idata_base import IDataBase
from services.ipost_repo import IPostRepo
from services.idatabase_config import IDataBaseConfig
from services.database_config import DataBaseConfig
from services.iusers_repo import IUsersRepo
from services.users_in_memo import Users
from services.users_db_repo import UsersDb
from services.mock_db_config import MockDbConfig, MockConfig

class Container:
    dependencies = {
        IPostRepo : IDataBase,
        IDataBase : (IDataBaseConfig, IDataBaseUpgrade),
        IDataBaseConfig : None,
        IDataBaseUpgrade : IDataBaseConfig,
        IUsersRepo : IPostRepo,
        IAuthentication : (IUsersRepo, IPassHash),
        IPassHash : None,
        }

    prod_services = {
        IPostRepo : PostsDb,
        IDataBase : DataBase,
        IDataBaseConfig : DataBaseConfig,
        IDataBaseUpgrade : DataBaseUpgrade,
        IUsersRepo : UsersDb,
        IAuthentication : Authentication,
        IPassHash : PassHash
        }

    test_services = {
        IPostRepo : Posts,
        IDataBase: DataBase,
        IDataBaseConfig: MockDbConfig,
        IUsersRepo : Users,
        IAuthentication : Authentication,
        IPassHash: PassHash,
        IDataBaseUpgrade : DataBaseUpgrade}

    def __init__(self, is_test):
        self.items = self.get(is_test)
    
    def get(self, is_test : bool) -> dict:
        if is_test:
            self.dependencies["IPostRepo"] = None
        return self.test_services if is_test else self.prod_services
   