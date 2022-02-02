from email import contentmanager


class Post:
    def __init__(self, auth, title, content):
        self.auth = auth
        self.title = title
        self.content = content        

    def getPreviewd(self):
        preview = self.content[:125]
        return preview