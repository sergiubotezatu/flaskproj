
class DBSettings:
    def __init__(self, section, dbname, user, password, host):
        self.section : str = section
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host

    def to_dict(self) -> dict:
        return {"dbname" : self.dbname,
                "user": self.user,
                "password": self.password,
                "host" : self.host}

    def to_DB_URI(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}/{self.dbname}"
