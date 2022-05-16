from services.auth.session_manager import SessionMngr
from services.database.sqlalchemy import SqlAlchemy
from services.interfaces.Ipassword_hash import IPassHash
from services.database.db_upgrade import DataBaseUpgrade
from services.interfaces.iauthentication import IAuthentication
from services.interfaces.iauthorization import IAuthorization
from services.auth.authentication import Authentication
from services.interfaces.idb_upgrade import IDataBaseUpgrade
from services.auth.authorization import Authorization
from services.interfaces.ifilters import IFilters
from services.interfaces.isession_mngr import ISessionMNGR
from services.posts.filters import Filters
from services.posts.sqlalchemy_posts import SqlAlchemyPosts
from services.users.passhash import PassHash
from services.posts.posts_db_repo import PostsDb
from services.posts.posts_in_memo import Posts
from services.database.database import DataBase
from services.interfaces.idata_base import IDataBase
from services.interfaces.ipost_repo import IPostRepo
from services.interfaces.idatabase_config import IDataBaseConfig
from services.database.database_config import DataBaseConfig
from services.interfaces.iusers_repo import IUsersRepo
from services.users.sqlalchemy_users import SqlAlchemyUsers
from services.users.users_db_repo import UsersDb
from services.users.users_in_memo import Users
from services.database.mock_db_config import MockDbConfig, MockUpgrade

class Container:
    dependencies = {
        IPostRepo : (IDataBase,),
        IDataBase : (IDataBaseConfig, IDataBaseUpgrade),
        IDataBaseConfig : None,
        IDataBaseUpgrade : (IDataBaseConfig,),
        IUsersRepo : (IDataBase,),
        IAuthentication : (IUsersRepo, IPassHash),
        IAuthorization : (IAuthentication,),
        IPassHash : None,
        ISessionMNGR : None,
        IFilters : (IPostRepo,)
        }

    prod_services = {
        IPostRepo : PostsDb,
        IDataBase : DataBase,
        IDataBaseConfig : DataBaseConfig,
        IDataBaseUpgrade : DataBaseUpgrade,
        IUsersRepo : UsersDb,
        IAuthentication : Authentication,
        IPassHash : PassHash,
        IAuthorization : Authorization,
        ISessionMNGR : SessionMngr,
        IFilters : Filters
        }

    test_services = {
        IPostRepo : Posts,
        IDataBase: DataBase,
        IDataBaseConfig: MockDbConfig,
        IUsersRepo : Users,
        IAuthentication : Authentication,
        IPassHash: PassHash,
        IDataBaseUpgrade : MockUpgrade,
        IAuthorization : Authorization,
        ISessionMNGR : SessionMngr,
        IFilters : Filters}

    sql_alchemy_services = {
        IPostRepo : SqlAlchemyPosts,
        IUsersRepo : SqlAlchemyUsers,
        IDataBase : SqlAlchemy
    }

    def __init__(self, is_test : bool, with_orm : bool):
        self.items = self.get(is_test, with_orm)
    
    def get(self, is_test : bool, with_orm : bool) -> dict:
        if with_orm:
            self.prod_services.update(self.sql_alchemy_services)
        if is_test:
            self.dependencies[IPostRepo] = None
            self.dependencies[IUsersRepo] = (IPostRepo,)
            return self.test_services
        return self.prod_services
