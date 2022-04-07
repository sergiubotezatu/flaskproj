from configparser import ConfigParser
import os.path

class Config:
    def __init__(self):
        self.CONFIGFILE = "db_file.ini"
        
    def load(self, section) -> ConfigParser:
        if self.section_exists(section):
            parser = ConfigParser()
            parser.read(self.CONFIGFILE)
            return parser
        else:
            raise Exception(f"Section {section} not found in the {self.CONFIGFILE} file")
        
    def save(self, parser : ConfigParser):
        section = parser.sections()[0]
        params = f"[{section}]\n"
        for item in parser.items(section):
            params += f"{item[0]} = {item[1]}\n"
        with open(self.CONFIGFILE, "a") as writer:
            writer.write(params)
       
    def section_exists(self, section : str):
        parser = ConfigParser()
        if os.path.exists(self.CONFIGFILE):
            parser.read(self.CONFIGFILE)
            return parser.has_section(section)
        return False
