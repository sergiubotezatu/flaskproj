class Post:
    def __init__(self, auth, title, content):
        self.auth = auth
        self.title = title
        self.content = content        

    def getPreviewd(self):
        preview = self.content[:150]
        return preview

author = "Chandler Bing"
title = "Bath time"
content = ("It's so hard to care when you are this relaxed...but maybe you could post something.\n"
"Click me and start writting")
example = Post(author, title, content)