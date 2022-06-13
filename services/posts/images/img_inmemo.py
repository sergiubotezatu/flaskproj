from werkzeug.datastructures import FileStorage
from interfaces.iimages import Iimages

class ImagesOnDisk(Iimages):
    def __init__(self):
        self.DEFAULT = "/static/icons/noimage.jpg"
        self.pictures = []
       
    def add(self, pic : FileStorage):
        pass

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