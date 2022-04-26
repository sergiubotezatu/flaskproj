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
        new_section = parser.sections()[0]
        existing_params = ConfigParser()
        existing_params.read(self.CONFIGFILE)
        params = ""
        if self.section_exists(new_section):
            existing_params.pop(new_section)
        existing_params.add_section(new_section)
        for item in parser.items(new_section):
            existing_params.set(new_section, item[0], item[1])
        for section in existing_params.sections():
            params += f"[{section}]\n"
            for item in existing_params.items(section):
                params += f"{item[0]} = {item[1]}\n"
        with open(self.CONFIGFILE, "w+") as writer:
                writer.write(params)
       
    def section_exists(self, section : str):
        parser = ConfigParser()
        if os.path.exists(self.CONFIGFILE):
            parser.read(self.CONFIGFILE)
            return parser.has_section(section)
        return False
