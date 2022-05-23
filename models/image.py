import psycopg2


class Image:
    def __init__(self, data, mime_type):
        self.data = data
        self.mime_type = mime_type

    @classmethod
    def default(cls):
        img = open("static\\icons\\noimage.png", "rb").read()
        return cls(img, "image/png")