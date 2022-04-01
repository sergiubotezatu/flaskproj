from services.interfaces.Ipassword_hash import IPassHash
from services.database.db_upgrade import DataBaseUpgrade
from services.interfaces.iauthentication import IAuthentication
from services.users.authentication import Authentication
from services.interfaces.idb_upgrade import IDataBaseUpgrade
from services.users.passhash import PassHash
from services.posts.posts_db_repo import PostsDb
from services.posts.posts_in_memo import Posts
from services.database.database import DataBase
from services.interfaces.idata_base import IDataBase
from services.interfaces.ipost_repo import IPostRepo
from services.interfaces.idatabase_config import IDataBaseConfig
from services.database.database_config import DataBaseConfig
from services.interfaces.iusers_repo import IUsersRepo
from services.users.users_in_memo import Users
from services.users.users_db_repo import UsersDb
from services.database.mock_db_config import MockDbConfig

class Container:
    dependencies = {
        IPostRepo : IDataBase,
        IDataBase : (IDataBaseConfig, IDataBaseUpgrade),
        IDataBaseConfig : None,
        IDataBaseUpgrade : IDataBaseConfig,
        IUsersRepo : IDataBase,
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
            self.dependencies["IUsersRepo"] = IPostRepo
        return self.test_services if is_test else self.prod_services
   