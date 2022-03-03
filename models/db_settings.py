
class DBSettings:
    def __init__(self, settings : list):
        self.section = settings[0]
        self.host = settings[1]
        self.dbname = settings[2]
        self.user = settings[3]
        self.password = settings[4]
