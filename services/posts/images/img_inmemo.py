import base64
from werkzeug.datastructures import FileStorage
from services.interfaces.iimages import Iimages

class ImagesInMemo(Iimages):
    def __init__(self):
        self.DEFAULT = "/static/icons/noimage.jpg"
        self.pictures = []
       
    def add(self, pic : FileStorage):
        extension = pic.mimetype.partition("/")[2]
        return (extension, base64.b64encode(pic.read()))

    def edit(self, pic : FileStorage, path : str):
        pass

    def get(self, file_name):
        pass

    def remove(self, file_name):
       pass

    def __add_on_disk(self, pic : FileStorage, file_name : str):
        pass

    def __create_name(self, pic):
        pass