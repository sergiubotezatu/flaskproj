from models.post import Post
from .Posts import Posts

blogPosts = Posts()

author = "Chandler Bing"
title = "Relaxi-cab"
content = ("It's so hard to care when you are this relaxed...but maybe you could post something.\n"
"Click me and start writing.")
placeholder = Posts()
placeholder.addPost(Post(author, title, content))