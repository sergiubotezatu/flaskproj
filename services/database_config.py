from configparser import ConfigParser
from models.db_settings import DBSettings
from services.idatabase_config import IDataBaseConfig
from services.resources import Services
from services.config import Config

class DataBaseConfig(Config, IDataBaseConfig):
    is_configured = False

    @Services.get
    def __init__(self):
        super().__init__()
        self.settings = None
        self.current_config = None
        self.load_existing_section()
                
    def add_settings(self, settings : DBSettings):
        self.settings = settings
                    
    def load(self):
        self.current_config = {}
        params = super().load()
        for param in params:
            self.current_config[param[0]] = param[1]
        
    def save(self):
        section = self.SECTION
        params = f"[{section}]\n"
        for options in self.setting_options:
            params += f"{options} = {getattr(self.settings, options)}\n"
        with open(self.CONFIGFILE, "w") as writer:
            writer.write(params)
        super().save()

    def load_existing_section(self):
        super().save()
        if self.section_exists():            
            self.load()
        self.is_configured = True
   
    def set_db_version(self, version):
        if self.parser.has_section("version"):
            self.parser.items("version")[0] = ("vers.", version)
        else:
            with open(self.CONFIGFILE, "a") as append:
                append.write(f"[version]\nvers. = {version}")
            super().save()
            
    def get_db_version(self):
        if self.parser.has_section("version"):
            return self.parser.items("version")[0][1]
        return "1.0"
