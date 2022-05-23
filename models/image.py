import psycopg2


class Image:
    def __init__(self, data, mime_type, name):
        self.data = data
        self.mime_type = mime_type
        self.name = name

    @classmethod
    def default(cls):
        img = open("static\\icons\\noimage.png", "rb").read()
        return cls(psycopg2.Binary(img), "image/png", "noimage.png")