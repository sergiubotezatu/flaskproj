from models.post import Post
from models.allPosts import allPosts

blogPosts = allPosts()
blogPreviews = allPosts()

author = "Chandler Bing"
title = "Bath time"
content = ("It's so hard to care when you are this relaxed...but maybe you could post something.\n"
"Click me and start writting")
example = Post(author, title, content)
placeholder = allPosts()
placeholder.addPost(example)