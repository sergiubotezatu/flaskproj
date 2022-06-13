import base64
from werkzeug.datastructures import FileStorage
from services.posts.images.img_ondisk import ImagesOnDisk
from services.interfaces.ipost_repo import IPostRepo
from services.interfaces.idata_base import IDataBase
from models.post import Post
from services.dependency_inject.injector import Services

class PostsDb(IPostRepo):
    @Services.get
    def __init__(self, db : IDataBase):
        self.__count = -1
        self.images = ImagesOnDisk()
        self.db = db
        
    @property
    def count(self):
        if self.__count == -1:
            return self.db.perform("""
            SELECT
            COUNT(Content)
            FROM blog_posts;
            """, fetch = "fetchone")[0]
        return self.__count

    @count.setter
    def count(self, value):
        self.__count = value
                
    def __len__(self):
        return self.count
    
    def add(self, post : Post, img : FileStorage):
        self.count += 1
        id = self.db.perform("""
        INSERT INTO blog_posts (PostID, Title, Content, Date, OwnerID, image)     
        VALUES (DEFAULT, %s, %s, %s, %s, %s)
        RETURNING PostID;
        """, post.title, post.content, post.created, post.owner_id, self.get_image(img), fetch = "fetchone")[0]
        return id

    def get_image(self, img : FileStorage):
        if img:
            return self.images.add(img)

    def replace(self, post : Post, img : FileStorage):
        if img != None:
            changed_name = self.images.edit(img, post.img_src)
            if changed_name:
                self.db.perform("""
                UPDATE blog_posts
                SET image= %s
                WHERE PostID = %s;""", changed_name, post.id)
        else:
            self.db.perform("""
                UPDATE blog_posts
                SET Title= %s, Content = %s, Date_modified = %s
                WHERE PostID = %s;
            """, post.title, post.content, post.created, post.id)

    def remove(self, id):
        self.count -= 1
        img = self.db.perform(f"SELECT image from blog_posts where PostID = {id}", fetch = "fetchone")[0]
        self.db.perform("""
            DELETE FROM blog_posts
            WHERE PostID = %s;
            """, id)   
        self.images.remove(img)
    
    def get(self, id, email = None) -> Post:
        displayed = None
        post = None
        if email != None:
            displayed = self.db.perform("""
            SELECT Content
            FROM
            deleted_users
            where Email = %s
            And deletedid = %s;
            """, email, id, fetch = "fetchone")
            post = Post(email, "No title", displayed[0])
        else:
            displayed = self.db.perform("""
            SELECT
                    u.Name,
                    p.title,
                    p.content,
                    u.OwnerID,
                    p.date,
                    p.Date_modified
                    p.Image
                FROM
                    blog_users u
                INNER JOIN blog_posts p
                    ON u.OwnerID = p.OwnerID
                    where p.PostID = %s;
                """, id, fetch = "fetchone")
            img = self.images.get(displayed[6])
            post = Post(displayed[0], displayed[1], displayed[2], owner_id = displayed[3], date = displayed[4], img_src=img)
            post.id = id
            post.modified = displayed[5]
        return post

    def get_all(self, page = 0, filters : list = [], max = 5):
        applied = ""
        offset = f"OFFSET {page * max - max}" if page != 0 else ""
        if len(filters) > 0:
            applied = "AND p.OwnerID IN ("
            for filter in filters:
                applied += filter if applied.endswith("(") else f", {filter}"
            applied = applied + ")"
        limit = f"LIMIT {max + 1}" if page > 0 else ""
        return self.__get_fetched(self.db.perform(f"""
            SET CLIENT_ENCODING TO 'utf8';
            SELECT p.PostID,
            u.Name,
            p.Title,
            SUBSTRING(p.Content, 1, 150),
            p.OwnerID,
            p.Date,
            i.file_data,
            i.mime_type
            FROM blog_posts p
            INNER JOIN blog_users u
            ON p.OwnerID = u.OwnerID
            INNER JOIN post_images i
            On p.postid = i.postid
            {applied}
            ORDER BY p.PostID DESC
            {offset}
            {limit};
            """, fetch = "fetchall"))

    def unarchive_content(self, id, name, email):
        result = self.db.perform("""
        SELECT Content
        FROM deleted_users
        WHERE Email = %s;
        """, email, fetch = "fetchall")
        i = 1
        for record in result:
            if record[0] != None:
                self.add(Post(name, f"{name}'s post {i}", record[0], owner_id = id))
                i += 1

    def __get_fetched(self, fetched):
        result = []
        count = 0
        if fetched != None:
            for post in fetched:
                count += 1
                result.append((post[0], Post(post[1], post[2], self.__cut_poem_newlines(post[3]), owner_id= post[4], date = post[5]), count))
        return result

    def __cut_poem_newlines(self, content):
        lines_count = content.count("\n")
        if lines_count > 0:
            chunk = lines_count * 3
            return content[:-chunk] + "[...]"
        return content + "[...]"
