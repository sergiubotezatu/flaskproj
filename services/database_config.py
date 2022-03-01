from configparser import ConfigParser
import encodings
from models.db_settings import DBSettings

class DataBaseConfig:
    def __init__(self):
        self.settings = None
        self.current_config = None
        self.setting_options = ["host", "databse", "user", "password"]
        self.CONFIGFILE = "db_file"
        self.parser = ConfigParser()        

    def add_settings(self, settings : DBSettings):
        self.settings = settings
                    
    def load(self):
        section = self.settings[0]
        self.parser.read(self.CONFIGFILE)
        db = {}
        if self.parser.has_section(section):
            params = self.parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception(f"Section {section} not found in the {self.CONFIGFILE} file")

        self.current_config = db

    def save(self):
        section = self.settings[0]
        params = "section\n"
        for options in self.setting_options:
            params += f"{options} = {getattr(self.settings, options)}\n"
        with open(self.CONFIGFILE, "w", encodings = "cp1251") as writer:
            writer.write(params)    
