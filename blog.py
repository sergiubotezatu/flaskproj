from __initblog__ import create_blog

blog = create_blog(with_orm = False)

if __name__ == ("__main__"):
    blog.run(debug = True)
