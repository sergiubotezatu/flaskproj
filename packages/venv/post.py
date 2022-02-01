class Post:

    def __init__(self, title, description, content, auth):
        self.title = title
        self.description = description
        self.text = content
        self.auth = auth           

    def checkPass(self, userPass):
        return self.__password == userPass