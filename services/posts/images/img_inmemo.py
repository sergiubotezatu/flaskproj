import base64
from werkzeug.datastructures import FileStorage
from services.interfaces.iimages import Iimages

class ImagesInMemo(Iimages):
    def __init__(self):
        self.DEFAULT = "static/images/noimage.jpg"
       
    def add(self, pic : FileStorage):
        extension = pic.mimetype.partition("/")[2]
        return (extension, base64.b64encode(pic.read()))

    def edit(self, pic : FileStorage):
        return self.add(pic)

    def get(self, file):
        if not file:
            return self.DEFAULT
        return f"'data:image/{file[0]};base64,{file[1]}'"

    def remove(self, file_name):
       pass   