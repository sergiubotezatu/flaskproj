from datetime import datetime

from models.image import Image

class Post:
    def __init__(self, auth, title, content, owner_id = 0, date = None, img = Image.default()):
        self.auth = auth
        self.title = title
        self.content = content
        self.owner_id = owner_id
        self.created = self.date_created(date)
        self.modified = ""
        self.id = 0
        self.img = img
        
    def date_created(self, date):
        if date == None:
            date = datetime.now().strftime("%d/%b/%y %H:%M:%S")
        return date

class Preview():
    def __init__(self, post):
        self.auth = post.auth
        self.title = post.title
        self.content = self.truncate(post.content)
        self.owner_id = post.owner_id
        self.created = post.created
        self.modified = post.modified
        self.img = post.img
        
    def truncate(self, content):
        lines_count = content[:150].count("\n")
        chunk = 150 - (lines_count * 3)
        return content[:chunk] + "[...]"
        