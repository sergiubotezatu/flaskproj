from unittest import mock
from services.interfaces.idatabase_config import IDataBaseConfig
from services.dependency_inject.injector import Services

class MockConfig:
    def __init__(self):
        pass

class MockDbConfig(MockConfig, IDataBaseConfig):
    is_configured = False

    @Services.get
    def __init__(self):
        pass
       
    def save(self, settings):
        pass

    def load(self):
        pass

    def get_db_version(self):
        pass

    def set_db_version(self, version):
        pass

    def section_exists(self, section : str):
        return True

