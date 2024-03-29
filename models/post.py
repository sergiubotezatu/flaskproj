from datetime import datetime

class Post:
    def __init__(self, auth, title, content, owner_id = 0, date = None, img_src : str = None):
        self.auth = auth
        self.title = title
        self.content = content
        self.owner_id = owner_id
        self.created = self.date_created(date)
        self.modified = ""
        self.id = 0
        self.img_src = img_src
        
    def date_created(self, date):
        if date == None:
            date = datetime.now().strftime("%d/%b/%y %H:%M:%S")
        return date

class Preview():
    def __init__(self, post : Post):
        self.auth = post.auth
        self.title = post.title
        self.content = self.truncate(post.content)
        self.owner_id = post.owner_id
        self.created = post.created
        self.modified = post.modified
        self.img_src = post.img_src
        
    def truncate(self, content):
        lines_count = content[:150].count("\n")
        chunk = 150 - (lines_count * 3)
        return content[:chunk] + "[...]"
        