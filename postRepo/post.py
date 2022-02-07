from datetime import datetime

class Post:
    def __init__(self, auth, title, content):
        self.auth = auth
        self.title = title
        self.content = content
        self.status = "created"
        self.date = self.dateCreated()    

    def dateCreated(self):
        return datetime.now().strftime("%d/%b/%y %H:%M:%S")

    def wasEditted(self):
        self.status = "editted"        

class Preview(Post):
    def __init__(self, auth, title, content):
        self.auth = auth
        self.title = title
        self.content = content[:150] + "[...]"
        self.date = self.dateCreated()