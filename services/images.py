import uuid
from werkzeug.datastructures import FileStorage

class Images:
    def __init__(self):
        self.PATH = "static/images"
        self.DEFAULT = "/static/images/noimage.png"
        self.just_added = None
       
    def add(self, pic : FileStorage):
        self.just_added = str(uuid.uuid4())
        extension = "." + pic.mimetype.partition("/")[2]
        self.just_added += extension
        self.__add_on_disk(pic, self.just_added)

    def edit(self, pic : FileStorage, path : str):
        image = pic.read()
        with open(path[1:], "wb") as writter:
            writter.write(image)

    def get(self, file_name):
        if file_name == None:
            return self.DEFAULT
        pic_path = f"/{self.PATH}/{file_name}"
        return pic_path

    def __add_on_disk(self, pic : FileStorage, file_name : str):
        image = pic.read()
        with open(self.PATH + f"/{file_name}", "wb") as writter:
            writter.write(image)
