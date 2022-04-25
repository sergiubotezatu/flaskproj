from unittest import mock
from models.db_settings import DBSettings
from services.interfaces.idatabase_config import IDataBaseConfig
from services.dependency_inject.injector import Services
from services.interfaces.idb_upgrade import IDataBaseUpgrade

class MockDbConfig(IDataBaseConfig):
    is_configured = False

    def __init__(self):
        pass
       
    def save(self, settings : DBSettings):
        pass

    def load(self):
        pass

    def get_db_version(self):
        pass

    def set_db_version(self, version):
        pass

    def section_exists(self, section : str):
        return True

class MockUpgrade(IDataBaseUpgrade):
    @Services.get
    def __init__(self, config : IDataBaseConfig):
        pass

    def is_latest_version(self):
        return True

    def upgrade(self):
        pass