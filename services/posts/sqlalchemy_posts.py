import base64
import PIL.Image
import io
from itsdangerous import base64_encode
from sqlalchemy import func
from models.image import Image
from services.database.sqlalchemy import SqlAlchemy
from services.interfaces.idata_base import IDataBase
from services.interfaces.ipost_repo import IPostRepo
from models.post import Post
from services.dependency_inject.injector import Services

class SqlAlchemyPosts(IPostRepo):
    @Services.get
    def __init__(self, orm : IDataBase):
        self.session = orm.session
        self.posts = orm.Posts
        self.__count = -1
        
    @property
    def count(self):
        if self.__count == -1:
            return self.session.query(self.posts.postid).count()
        return self.__count

    @count.setter
    def count(self, value):
        self.__count = value
                
    def __len__(self):
        return self.count
    
    def add(self, post : Post, img : Image):
        self.count += 1
        new_post = self.posts(title = post.title, content = post.content, date = post.created, ownerid = post.owner_id)
        self.session.add(new_post)
        self.session.commit()
        id = new_post.postid
        self.add_image(img, id)
        return new_post.postid

    def add_image(self, img : Image, id):
        new_img = SqlAlchemy.Images(postid = id, mime_type = img.mime_type, file_data = img.data)
        self.session.add(new_img)
        self.session.commit()

    def replace(self, id, post : Post = None, img : Image = None):
        dict_new = {}
        if img != None:
            dict_new = {"file_data" : img.data,
                        "mime_type" : img.mime_type}
            self.session.query(SqlAlchemy.Images).filter_by(postid = id).update(dict_new)
        else:
            dict_new = {"title" : post.title,
                        "content" : post.content,
                        "date_modified" : post.created}
            self.session.query(self.posts).filter_by(postid = id).update(dict_new)
        self.session.commit()

    def remove(self, id):
        self.session.query(self.posts).filter_by(postid = id).delete()
        self.session.commit()
    
    def get(self, id, email = None) -> Post:
        displayed = None
        post = None
        if email != None:
            displayed = self.session.query(SqlAlchemy.Deleted.content).filter_by(email = email, deletedid = id).first()
            post = Post(email, "No title", displayed[0])
        else:
            displayed = self.session.query\
                        (SqlAlchemy.Users.name,
                        self.posts.title,
                        self.posts.content,
                        SqlAlchemy.Users.ownerid,
                        self.posts.date,
                        self.posts.date_modified).\
                        join(SqlAlchemy.Users, SqlAlchemy.Users.ownerid == self.posts.ownerid).\
                        filter(self.posts.postid == id).first()
            post = Post(displayed[0], displayed[1], displayed[2], owner_id = displayed[3], date = displayed[4])
            post.modified = displayed[5]
        return post

    def get_img(self, id):
        data = self.session.query(SqlAlchemy.Images.file_data).filter_by(postid = id).first()
        return data[0]  

    def get_all(self, page = 0, filters : list = [], max = 5):
        posts = self.session.query\
            (self.posts.postid,
            SqlAlchemy.Users.name,
            self.posts.title,
            func.substr(self.posts.content, 0, 150),
            self.posts.ownerid,
            self.posts.date,
            SqlAlchemy.Images.file_data,
            SqlAlchemy.Images.mime_type).\
            join(SqlAlchemy.Users, SqlAlchemy.Users.ownerid == self.posts.ownerid).\
            join(SqlAlchemy.Images, SqlAlchemy.Images.postid == self.posts.postid).\
            order_by(self.posts.postid.desc())
        if len(filters) > 0:
            posts = posts.filter(self.posts.ownerid.in_(filters))
        if page > 0:
            offset = page * max - max
            posts = posts.offset(offset).limit(max + 1)
        return self.__get_fetched(posts.all())

    def unarchive_content(self, id, name, email):
        result = self.session.query(SqlAlchemy.Deleted.content).filter_by(email = email).all()
        i = 1
        for post in result:
            if post[0] != None:
                unarchived = Post(name, f"{name}'s post {i}", post[0], owner_id= id)
                self.add(unarchived)
                i += 1

    def __get_fetched(self, fetched):
        result = []
        count = 0
        if fetched != None:
            for post in fetched:
                count += 1
                img_data = Image(base64.b64encode(post[6]).decode(), post[7])
                result.append((post[0],
                Post(post[1], post[2], self.__cut_poem_newlines(post[3]), owner_id= post[4], date = post[5], img = img_data),
                count))
        return result

    def __cut_poem_newlines(self, content):
        lines_count = content.count("\n")
        if lines_count > 0:
            chunk = lines_count * 3
            return content[:-chunk] + "[...]"
        return content + "[...]"
