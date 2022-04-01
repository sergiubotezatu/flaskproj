from unittest import mock
from services.idatabase_config import IDataBaseConfig
from services.resources import Services

class MockConfig:
    def __init__(self):
        pass

class MockDbConfig(MockConfig, IDataBaseConfig):
    is_configured = False

    @Services.get
    def __init__(self):
        pass
       
    def save(self):
        pass

    def load(self):
        pass

    def add_settings(self):
        pass

    def get_db_version(self):
        pass

    def set_db_version(self):
        pass

