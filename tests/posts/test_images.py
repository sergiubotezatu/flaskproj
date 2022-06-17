import io
from flask import Flask
from pytest import fixture
from PIL import Image
import base64
import __init__
from services.posts.posts_in_memo import Posts
from tests.helpers import add_disposable_img_post, configure, generate_img, get_url_userid, log_user

BASE_POST = "/post/"

@fixture()
def client(data_base : Flask):
    return data_base.test_client()

@configure(True)
def test_text_only_posts_display_default_image(client):
    result = client.get(BASE_POST + "read/1/")
    assert '<img src = "/static/images/noimage.jpg">' in result.data.decode("UTF-8")  

@log_user(1, "Mark Doe", "Mark@mail", "regular")
@configure(True)
def test_create_post_with_new_img(client):
    pic = generate_img()
    post = {
        "author" : "Mark Doe",
        "title" : "Generic",
        "post" : "This is a test",
        "img" : pic[1]
        }
    creation = client.post(BASE_POST + "create", data = post, follow_redirects=False)
    displayed = base64.b64encode(pic[0].tobytes())
    id = get_url_userid(creation)
    result = client.get(BASE_POST + f"read/{id}/")
    assert displayed in result.data
    Posts().remove(id)
    
@log_user(1, "Mark Doe", "Mark@mail", "regular")
@configure(True)
def test_home_displays_images(client):
    pic = generate_img()
    id = add_disposable_img_post(client, pic[1])
    displayed = base64.b64encode(pic[0].tobytes())
    result = client.get("/")
    assert displayed in result.data
    assert "static/images/noimage.jpg" in result.data.decode("UTF-8")
    Posts().remove(id)

@log_user(1, "Mark Doe", "Mark@mail", "regular")
@configure(True)
def test_edit_default_image(client):
    pic = generate_img()
    edit = {
        "author" : "Mark Doe",
        "title" : "Generic",
        "post" : "This is a test",
        "img" : pic[1]
        }
    replace = client.post(BASE_POST + "edit/2/", data = edit, follow_redirects=False)
    displayed = base64.b64encode(pic[0].tobytes())
    id = get_url_userid(replace)
    result = client.get(BASE_POST + f"read/{id}/")
    assert displayed in result.data
    
@log_user(1, "Mark Doe", "Mark@mail", "regular")
@configure(True)
def test_edit_custom_image(client):
    init_pic = generate_img()[1]
    id = add_disposable_img_post(client, init_pic)
    new_file = Image.new('RGB', (250, 250), color = "#FFFFFF")
    new_byte_file = new_file.tobytes()
    new_img = (io.BytesIO(new_byte_file), "test.png")
    edit = {
        "author" : "Mark Doe",
        "title" : "Generic",
        "post" : "This is a test",
        "img" : new_img
        }
    client.post(BASE_POST + f"edit/{id}/", data = edit, follow_redirects=False)
    displayed = base64.b64encode(new_file.tobytes())
    result = client.get(BASE_POST + f"read/{id}/")
    assert displayed in result.data
    Posts().remove(id)