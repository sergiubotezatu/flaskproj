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
                        
    def load(self, section) -> DBSettings:
        self.current_config = {}
        params = super().load(section).items(section)
        settings = [section]
        for param in params:
            settings.append(param[1])
        DataBaseConfig.is_configured = True
        return DBSettings(settings)
        
    def save(self, settings : DBSettings):
        if not self.section_exists(settings.section):
            parser = ConfigParser()
            parser.add_section(settings.section)
            for i in range(4):
                parser.set(settings.section,
                self.setting_options[i] ,settings.configuration[self.setting_options[i]])
            super().save(parser)        

    def set_db_version(self, version):
        parser = ConfigParser()
        if self.section_exists("version"):
            with open(self.CONFIGFILE, 'r+') as editter:
                line = editter.readline()
                while line:
                    if line.startswith("vers."):
                        editter.write(f"vers. = {version}")
        else:
            with open(self.CONFIGFILE, "a") as append:
                parser.add_section("version")
                parser.set("version", "vers.", version)
            super().save(parser)
            
    def get_db_version(self):
        parser = ConfigParser()
        if self.section_exists("version"):
            parser.read(self.CONFIGFILE)
            return parser.get("version", "vers.")
        return "1.0"
