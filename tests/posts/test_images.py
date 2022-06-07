import unittest
from __initblog__ import create_blog
from services.interfaces.ipost_repo import IPostRepo
from tests.test_helpers import RepoMngr, configure, getClient, log_user
from flask.testing import FlaskClient
from werkzeug.datastructures import FileStorage
import glob
import os

class ImageTests(unittest.TestCase):
    blog = create_blog(is_test_app = True, with_orm = False)
    BASE_POST = "/post/"
    posts = RepoMngr(IPostRepo)
    
    @getClient
    @log_user(1, "Mark Doe", "MDoe@gmail", "admin")
    @configure(True)
    def test_text_only_posts_display_default_image(self, client : FlaskClient = None):
        post = {
        "author" : "Mark Doe",
        "title" : "Generic",
        "post" : "This is a test"
        }        
        creation = client.post(self.BASE_POST + "create", data = post, follow_redirects=True)
        self.assertIn("/static/images/noimage.jpg", creation.data.decode("UTF-8"))        

    @getClient
    @log_user(1, "Mark Doe", "MDoe@gmail", "admin")
    @configure(True)
    def test_create_post_with_new_img_saves_on_disk(self, client : FlaskClient = None):
        file = open("img.png", "rb")
        img = FileStorage(file)
        img.save("img.png")
        post = {
        "author" : "Mark Doe",
        "title" : "Generic",
        "post" : "This is a test",
        "img" : img
        }        
        client.post(self.BASE_POST + "create", data = post, follow_redirects=True)
        folder_path = r"static\images"
        file_type = r"\*png"
        files = glob.glob(folder_path + file_type)
        last_added = max(files, key=os.path.getctime)
        with open(last_added, "rb") as saved:
            with open("img.png", "rb") as created:
                self.assertEqual(saved.read(), created.read())
        os.remove(last_added)
        
    @getClient
    @log_user(1, "Mark Doe", "MDoe@gmail", "admin")
    @configure(True)
    def test_read_post_displays_image(self, client : FlaskClient = None):
        file = open("img.png", "rb")
        img = FileStorage(file)
        img.save("img.png")
        post = {
        "author" : "Mark Doe",
        "title" : "Generic",
        "post" : "This is a test",
        "img" : img
        }
        creation = client.post(self.BASE_POST + "create", data = post, follow_redirects=True)
        folder_path = r"static\images"
        file_type = r"\*png"
        files = glob.glob(folder_path + file_type)
        last_added = max(files, key=os.path.getctime)
        self.assertIn(last_added.replace("\\", "/"), creation.data.decode("UTF-8"))
        os.remove(last_added)       

    @getClient
    @log_user(1, "Mark Doe", "MDoe@gmail", "admin")
    @configure(True)
    def test_edit_default_image(self, client : FlaskClient = None):
        post = {
        "author" : "Mark Doe",
        "title" : "Generic",
        "post" : "This is a test"
        }        
        creation = client.post(self.BASE_POST + "create", data = post, follow_redirects=False)
        url = creation.location
        id_index = url.rfind("/") + 1
        id = url[id_index:]
        file = open("img.png", "rb")
        img = FileStorage(file)
        img.save("img.png")
        edit =  {
        "author" : "Mark Doe",
        "title" : "Generic",
        "post" : "This is a test",
        "img" : img
        }
        edit = client.post(self.BASE_POST + f"edit/{id}", data = edit, follow_redirects=True)
        folder_path = r"static\images"
        file_type = r"\*png"
        files = glob.glob(folder_path + file_type)
        last_added = max(files, key=os.path.getctime)
        self.assertIn(last_added.replace("\\", "/"), edit.data.decode("UTF-8"))
        os.remove(last_added)

    @getClient
    @log_user(1, "Mark Doe", "MDoe@gmail", "admin")
    @configure(True)
    def test_edit_custom_image(self, client : FlaskClient = None):
        init_file = open("img.png", "rb")
        init_img = FileStorage(init_file)
        init_img.save("img.png")
        post = {
        "author" : "Mark Doe",
        "title" : "Generic",
        "post" : "This is a test",
        "img" : init_img
        }
        creation = client.post(self.BASE_POST + "create", data = post, follow_redirects=False)
        url = creation.location
        id_index = url.rfind("/") + 1
        id = url[id_index:]
        file = open("img.png", "rb")
        img = FileStorage(file)
        img.save("img.png")
        edit =  {
        "author" : "Mark Doe",
        "title" : "Generic",
        "post" : "This is a test",
        "img" : img
        }
        edit = client.post(self.BASE_POST + f"edit/{id}", data = edit, follow_redirects=True)
        folder_path = r"static\images"
        file_type = r"\*png"
        files = glob.glob(folder_path + file_type)
        last_added = max(files, key=os.path.getctime)
        self.assertIn(last_added.replace("\\", "/"), edit.data.decode("UTF-8"))
        os.remove(last_added)

    @getClient
    @log_user(1, "Mark Doe", "MDoe@gmail", "admin")
    @configure(True)
    def test_deletting_post_deletes_image(self, client : FlaskClient = None):
        file = open("img.png", "rb")
        img = FileStorage(file)
        img.save("img.png")
        post = {
        "author" : "Mark Doe",
        "title" : "Generic",
        "post" : "This is a test",
        "img" : img
        }
        creation = client.post(self.BASE_POST + "create", data = post, follow_redirects=False)
        url = creation.location
        id_index = url.rfind("/") + 1
        id = url[id_index:]
        folder_path = r"static\images"
        file_type = r"\*png"
        files = glob.glob(folder_path + file_type)
        last_added = max(files, key=os.path.getctime)
        car = client.post(self.BASE_POST + f"read/{id}/", data = {"postID" : id})
        self.assertEqual(os.path.exists(last_added), False)

if __name__ == "__main__":
    unittest.main()