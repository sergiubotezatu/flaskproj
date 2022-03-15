from unittest import mock
from services.resources import Services

class MockDbConfig:
    @staticmethod
    @Services.get
    def mocked_db_config(self):
        with mock.patch("services.database_config.DataBaseConfig") as mocked_config:
            mocked_config.is_configured = False
            mocked_config.add_settings = MockDbConfig.mock_add_settings
            mocked_config.load = MockDbConfig.mock_load 
            return mocked_config

    @staticmethod
    def mock_add_settings(settings):
        pass

    @staticmethod
    def mock_load():
        pass