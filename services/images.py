import uuid
from werkzeug.datastructures import FileStorage
import os

class Images:
    def __init__(self):
        self.PATH = "static/images"
        self.DEFAULT = "/static/images/noimage.jpg"
       
    def add(self, pic : FileStorage):
        just_added = self.__create_name(pic)
        self.__add_on_disk(pic, just_added)
        return just_added

    def edit(self, pic : FileStorage, path : str):
        image = pic.read()
        is_default = "noimage" in path
        name = self.__create_name(pic)
        new_path = path[1:] if not is_default else self.PATH + f"/{name}"
        with open(new_path, "wb") as writter:
            writter.write(image)
        if is_default:
            return name
        else:
            return None

    def get(self, file_name):
        if file_name == None:
            return self.DEFAULT
        pic_path = f"/{self.PATH}/{file_name}"
        return pic_path

    def remove(self, file_name):
        if file_name:
            os.remove(f"{self.PATH}/{file_name}")

    def __add_on_disk(self, pic : FileStorage, file_name : str):
        image = pic.read()
        with open(self.PATH + f"/{file_name}", "wb") as writter:
            writter.write(image)

    def __create_name(self, pic):
        extension = "." + pic.mimetype.partition("/")[2]
        return str(uuid.uuid4()) + extension
