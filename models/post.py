from datetime import datetime

class Post:
    def __init__(self, auth, title, content, date = None):
        self.auth = auth
        self.title = title
        self.content = content
        self.created = self.date_created(date)
        self.modified = ""
        
    def date_created(self, date):
        if date == None:
            date = datetime.now().strftime("%d/%b/%y %H:%M:%S")
        return date

    def edit(self, editted):
        self.auth = editted.auth
        self.title = editted.title
        self.content = editted.content
        self.modified = editted.created

class Preview():
    def __init__(self, post):
        self.auth = post.auth
        self.title = post.title
        self.content = self.truncate(post.content)
        self.created = post.created
        self.modified = post.modified

    def truncate(self, content):
        lines_count = content[:150].count("\n")
        chunk = 150 - (lines_count * 3)
        return content[:chunk] + "[...]"
        