from configparser import ConfigParser
from models.db_settings import DBSettings

class DataBaseConfig:
    def __init__(self):
        self.settings = None
        self.current_config = None
        self.setting_options = ["dbname", "user", "password", "host"]
        self.CONFIGFILE = "db_file"
        self.parser = ConfigParser()

    def add_settings(self, settings : DBSettings):
        self.settings = settings
                    
    def load(self):
        section = self.settings.section
        self.parser.read(self.CONFIGFILE)
        self.current_config = {}
        if self.parser.has_section(section):
            params = self.parser.items(section)
            for param in params:
                self.current_config[param[0]] = param[1]
        else:
            raise Exception(f"Section {section} not found in the {self.CONFIGFILE} file")

    def save(self):
        section = self.settings.section
        params = f"[{section}]\n"
        for options in self.setting_options:
            params += f"{options} = {getattr(self.settings, options)}\n"
        with open(self.CONFIGFILE, "w") as writer:
            writer.write(params)    
    