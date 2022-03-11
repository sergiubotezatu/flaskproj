from importlib.util import spec_from_file_location
from unittest import mock
from resources.posts_db_repo import PostsDb
from resources.posts_in_memo import Posts
from resources.database import DataBase
from resources.idata_base import IDataBase
from resources.ipost_repo import IPostRepo
from resources.idatabase_config import IDataBaseConfig
from resources.database_config import DataBaseConfig
from resources.services import Services

@mock.patch("resources.database_config.DataBaseConfig", "is_configured", True)
@Services.get
def mocked_db_config(mocked):
    mocked = mock.MagicMock(spec= ["add_settings"])
    return mocked.return_value

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
            IDataBase: DataBase,
            IDataBaseConfig: mocked_db_config}
        
    def get(self, is_test : bool) -> dict:
        return self.test_services if is_test else self.prod_services
