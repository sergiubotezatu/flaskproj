from datetime import datetime
from pickletools import read_bytes4

class Post:
    def __init__(self, auth, title, content):
        self.auth = auth
        self.title = title
        self.content = content
        self.date = self.dateCreated()

    def dateCreated(self):
        createdOn = datetime.now().strftime("%d/%b/%y %H:%M:%S")
        return (createdOn, "")
    
    def edit(self, editted):
        self.auth = editted.auth
        self.title = editted.title
        self.content = editted.content
        self.date = (self.date[0], ("modified: " + editted.date[0]))

class Preview(Post):
    def __init__(self, post):
        self.auth = post.auth
        self.title = post.title
        self.content = post.content[:150] + "[...]"
        self.date = self.displayDate(post.date[0], post.date[1])

    def displayDate(self, created, modified):
        return created if modified == "" else modified[10:]