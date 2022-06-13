from services.interfaces.iimages import Iimages
from services.posts.posts_in_memo import Posts
from models.post import Post

def placeholder():
    AUTHOR = "Chandler Bing"
    TITLE = "Relaxi-cab"
    CONTENT = ("It's so hard to care when you are this relaxed...but maybe you could post something.\n"
    "Click me and start writing.")
    placeholder = Posts(Iimages)
    placeholder.add(Post(AUTHOR, TITLE, CONTENT))
    return placeholder
