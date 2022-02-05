from flask import flask
from datetime import datetime

class Post:
    def __init__(self, auth, title, content):
        self.auth = auth
        self.title = title
        self.content = content 
        self.date = self.dateCreated()     

    def getPreviewd(self):
        preview = self.content[:150]
        return preview

    def dateCreated(self):
        utc = datetime.datetime.now()
        extraZones = datetime.timedelta(hours = 2)
        return utc + extraZones 
