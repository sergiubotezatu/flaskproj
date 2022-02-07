from .post import Post
from .Posts import Posts

blogPosts = Posts()
blogPreviews = Posts()

author = "Chandler Bing"
title = "Bath time"
content = ("It's so hard to care when you are this relaxed...but maybe you could post something.\n"
"Click me and start writing.")
example = Post(author, title, content)
placeholder = Posts()
placeholder.addPost(example)