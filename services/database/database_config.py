from configparser import ConfigParser
from models.db_settings import DBSettings
from services.interfaces.idatabase_config import IDataBaseConfig
from services.dependency_inject.injector import Services
from services.database.config import Config

class DataBaseConfig(Config, IDataBaseConfig):
    is_configured = False

    def __init__(self):
        super().__init__()
        self.setting_options = ["dbname", "user", "password", "host"]
        self.DB_SETTINGS = "postgresql"
        self.VERSION = "version"
                        
    def load(self) -> DBSettings:
        self.current_config = {}
        section = self.DB_SETTINGS
        params = super().load(section).items(section)
        settings = [section]
        for param in params:
            settings.append(param[1])
        DataBaseConfig.is_configured = True
        return DBSettings(*settings)
        
    def save(self, settings : DBSettings):
        if not self.section_exists(settings.section):
            dict_settings = settings.to_dict()
            parser = ConfigParser()
            parser.add_section(settings.section)
            for i in range(4):
                parser.set(settings.section,
                self.setting_options[i] ,dict_settings[self.setting_options[i]])
            super().save(parser)        

    def set_db_version(self, version):
        parser = ConfigParser()
        parser.add_section(self.VERSION)
        parser.set(self.VERSION, "vers.", version)
        super().save(parser)

    def get_db_version(self):
        parser = ConfigParser()
        if self.section_exists(self.VERSION):
            parser.read(self.CONFIGFILE)
            return parser.get(self.VERSION, "vers.")
        return "1.0"
