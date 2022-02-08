import blog
import unittest
from flask import request, jsonify
import requests

class test_BlogRequests(unittest.TestCase):
    def setUp(self):
        blog.blog.testing = True
        self.app = blog.blog.test_client()

    HOME_URL = "http://127.0.0.1:5000/"
    CREATE_URL = "http://127.0.0.1:5000/post/create" 

    def test_HomeRequest(self):
        testHome = requests.get(self.HOME_URL)
        self.assertEqual(testHome.status_code, 200)

    def test_CreateRequest(self):
        testCreate = requests.get(self.CREATE_URL)
        self.assertEqual(testCreate.status_code, 200)

class test_CreatePost(unittest.TestCase):
    def setUp(self):
        blog.blog.testing = True
        self.app = blog.blog.test_client()
    CREATE_URL = "http://127.0.0.1:5000/post/create"
    POST = {
        "auth" : "John Doe",
        "title" : "Generic",
        "post" : "This is a test"
    }

    def test_CreateNewPost(self):
        testPost = self.app.post(self.CREATE_URL, data = self.POST)
        self.assertEqual(testPost.status_code, 201)

if __name__ == "__main__":
    unittest.main()