from sqlalchemy import func
from services.database.sqlalchemy import SqlAlchemy
from services.interfaces.iimages import Iimages
from services.interfaces.idata_base import IDataBase
from services.interfaces.ipost_repo import IPostRepo
from models.post import Post
from services.dependency_inject.injector import Services
from werkzeug.datastructures import FileStorage


class SqlAlchemyPosts(IPostRepo):
    @Services.get
    def __init__(self, orm: IDataBase, images: Iimages):
        self.orm = orm
        self.images = images
        self.__count = -1

    @property
    def count(self):
        if self.__count == -1:
            return self.orm.session.query(self.orm.Posts.postid).count()
        return self.__count

    @count.setter
    def count(self, value):
        self.__count = value

    def __len__(self):
        return self.count

    def add(self, post: Post, img: FileStorage):
        self.count += 1
        new_post = self.orm.Posts(title=post.title,
                                  content=post.content,
                                  date=post.created,
                                  ownerid=post.owner_id,
                                  image=self.get_image(img))
        self.orm.session.add(new_post)
        self.orm.session.commit()
        return new_post.postid

    def get_image(self, img: FileStorage):
        if img:
            return self.images.add(img)

    def replace(self, post: Post, img: FileStorage):
        dict_new = {"title": post.title,
                    "content": post.content,
                    "date_modified": post.created}
        if img:
            changed_name = self.images.edit(img, post.img_src)
            if changed_name:
                dict_new.update({"image": changed_name})
        self.orm.session.query(self.orm.Posts).filter_by(postid=post.id).update(dict_new)
        self.orm.session.commit()

    def remove(self, id):
        img = self.orm.session.query(self.orm.Posts.image).filter_by(postid=id).first()
        self.orm.session.query(self.orm.Posts).filter_by(postid=id).delete()
        self.orm.session.commit()
        self.images.remove(img[0])

    def get(self, id, email=None) -> Post:
        displayed = None
        post = None
        if email != None:
            displayed = self.orm.session.query(SqlAlchemy.Deleted.content).filter_by(email=email, deletedid=id).first()
            post = Post(email, "No title", displayed[0])
        else:
            displayed = self.orm.session.query \
                (SqlAlchemy.Users.name,
                 self.orm.Posts.title,
                 self.orm.Posts.content,
                 SqlAlchemy.Users.ownerid,
                 self.orm.Posts.date,
                 self.orm.Posts.date_modified,
                 self.orm.Posts.image). \
                join(SqlAlchemy.Users, SqlAlchemy.Users.ownerid == self.orm.Posts.ownerid). \
                filter(self.orm.Posts.postid == id).first()
            if displayed:
                img = self.images.get(displayed[6])
                post = Post(displayed[0],
                            displayed[1],
                            displayed[2],
                            owner_id=displayed[3],
                            date=displayed[4],
                            img_src=img)
                post.id = id
                post.modified = displayed[5]
        return post

    def get_all(self, page=0, filters: list = [], max=5):
        posts = self.orm.session.query \
            (self.orm.Posts.postid,
             SqlAlchemy.Users.name,
             self.orm.Posts.title,
             func.substr(self.orm.Posts.content, 0, 150),
             self.orm.Posts.ownerid,
             self.orm.Posts.date,
             self.orm.Posts.image). \
            join(SqlAlchemy.Users, SqlAlchemy.Users.ownerid == self.orm.Posts.ownerid). \
            order_by(self.orm.Posts.postid.desc())
        if len(filters) > 0:
            posts = posts.filter(self.orm.Posts.ownerid.in_(filters))
        if page > 0:
            offset = page * max - max
            posts = posts.offset(offset).limit(max + 1)
        return self.__get_fetched(posts.all())

    def unarchive_content(self, id, name, email):
        result = self.orm.session.query(SqlAlchemy.Deleted.content).filter_by(email=email).all()
        i = 1
        for post in result:
            if post[0] != None:
                unarchived = Post(name, f"{name}'s post {i}", post[0], owner_id=id)
                self.add(unarchived)
                i += 1

    def __get_fetched(self, fetched):
        result = []
        count = 0
        if fetched is not None:
            for post in fetched:
                count += 1
                img = self.images.get(post[6])
                result.append((post[0],
                               Post(post[1], post[2], self.__cut_poem_newlines(post[3]), owner_id=post[4], date=post[5],
                                    img_src=img),
                               count))
        return result

    def __cut_poem_newlines(self, content):
        lines_count = content.count("\n")
        if lines_count > 0:
            chunk = lines_count * 3
            return content[:-chunk] + "[...]"
        return content + "[...]"
