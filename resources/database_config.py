from configparser import ConfigParser
from models.db_settings import DBSettings
from resources.idatabase_config import IDataBaseConfig
from resources.services import Services

class DataBaseConfig(IDataBaseConfig):
    is_configured = False

    @Services.get
    def __init__(self):
        self.settings = None
        self.current_config = None
        self.setting_options = ["dbname", "user", "password", "host"]
        self.CONFIGFILE = "db_file"
        self.parser = ConfigParser()

    def add_settings(self, settings : DBSettings):
        self.settings = settings
                    
    def load(self):
        section = self.settings.SECTION
        self.parser.read(self.CONFIGFILE)
        self.current_config = {}
        if self.parser.has_section(section):
            params = self.parser.items(section)
            for param in params:
                self.current_config[param[0]] = param[1]
        else:
            raise Exception(f"Section {section} not found in the {self.CONFIGFILE} file")
        self.edit_config_status()

    def save(self):
        section = self.settings.SECTION
        params = f"[{section}]\n"
        for options in self.setting_options:
            params += f"{options} = {getattr(self.settings, options)}\n"
        with open(self.CONFIGFILE, "w") as writer:
            writer.write(params)

    @classmethod
    def edit_config_status(cls):
        cls.is_configured = True