from services.interfaces.idatabase_config import IDataBaseConfig
from services.dependency_inject.injector import Services
from services.database.upgrade_queries import get_queries

class DataBaseUpgrade:
    @Services.get
    def __init__(self, config : IDataBaseConfig):
        self.config = config
        self.last_version = "1.5"
        self.current_version = self.config.get_db_version()
        
    def is_latest_version(self):
        return self.current_version == self.last_version

    def upgrade(self):
        queries = get_queries()
        i = int(self.current_version[-1:])
        self.config.set_db_version(self.last_version)
        while i < int(self.last_version[-1:]):
            for upgrades in queries[i]:
                yield upgrades
            i += 1