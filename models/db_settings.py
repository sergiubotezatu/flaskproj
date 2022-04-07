
class DBSettings:
    def __init__(self, settings : list):
        self.section : str = settings[0]
        self.configuration = {"dbname" : settings[1],
                            "user": settings[2],
                            "password":settings[3],
                            "host" : settings[4]}
