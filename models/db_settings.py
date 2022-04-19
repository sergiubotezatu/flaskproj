
class DBSettings:
    def __init__(self, settings : list):
        self.section : str = settings[0]
        self.dbname = settings[1]
        self.user = settings[2]
        self.password = settings[3]
        self.host = settings[4]

    def to_dict(self):
        return {"dbname " : self.dbname,
                "user": self.user,
                "password": self.password,
                "host" : self.host}
