from datetime import datetime

class Post:
    def __init__(self, auth, title, content):
        self.auth = auth
        self.title = title
        self.content = content
        self.date = self.date_created()
        
    def date_created(self):
        created_on = datetime.now().strftime("%d/%b/%y %H:%M:%S")
        return (created_on, "")

    def edit(self, editted):
        self.auth = editted.auth
        self.title = editted.title
        self.content = editted.content
        self.date = (self.date[0], ("modified: " + editted.date[0]))

class Preview():
    def __init__(self, post):
        self.auth = post.auth
        self.title = post.title
        self.content = self.truncate(post.content)
        self.date = self.display_date(post.date[0], post.date[1])

    def display_date(self, created, modified):
        return created if modified == "" else modified[10:]

    def truncate(self, content):
        lines_count = content[:150].count("\n")
        chunk = 150 - (lines_count * 3)
        return content[:chunk] + "[...]"
        