

def __read_all_inactive():
    return """
    SELECT d.Content,
    CASE
    WHEN CHAR_LENGTH(d.Content) > 150 THEN SUBSTRING(d.Content, 1, 150)
    ELSE d.Content
    END AS Preview 
    FROM deleted_users AS d
    WHERE Email = %s
    """

def __insert_post():
        return """
        INSERT INTO blog_posts (PostID, Title, Content, Date, OwnerID)     
        VALUES (DEFAULT, %s, %s, %s, %s)
        RETURNING PostID;
        """

def __insert_user():
    return """
    INSERT INTO blog_users      
    VALUES (DEFAULT, %s, %s, %s, %s)
    RETURNING OwnerID;
    """

def __update_user():
    return """
        UPDATE blog_users
        SET Name = %s, Email= %s, Date_modified = %s
        WHERE OwnerID = %s;
        UPDATE blog_posts
        SET Author = blog_users.Name
        FROM blog_users
        WHERE blog_posts.OwnerID = blog_users.OwnerID AND blog_posts.OwnerID = %s;
        """

def __update_post():
        return """
            UPDATE blog_posts
            SET Title= %s, Content = %s, Date_modified = %s
            WHERE PostID = %s;
        """

def __change_password():
    return """
        UPDATE blog_users
        SET Password = %s
        WHERE OwnerID = %s;
    """

def __archive():
    return """
    INSERT INTO deleted_users
    SELECT u.Email, p.Content 
    FROM blog_posts p
    RIGHT JOIN blog_users u ON p.OwnerId = u.OwnerID
    WHERE u.OwnerID = %s;
    """

def __delete_user():
    return """
        DELETE FROM 
        blog_users
        WHERE OwnerID = %s;
        """

def __delete_post():
        return """
            DELETE FROM blog_posts
            WHERE PostID = %s;
            """

def __get_user_by_identifier(identifier : str):
    return f"""
    SELECT *
    FROM blog_users
    WHERE {identifier} = """ + "%s"

def __get_all_users():
    return """
    SELECT OwnerID, Name
    FROM blog_users
    ORDER BY OwnerID DESC;
    """

def __get_removed_users():
    return """
    SELECT DISTINCT Email
    FROM deleted_users
    ;
    """

def __has_user():
    return """
    SELECT EXISTS(
        SELECT OwnerID
        FROM blog_users
        WHERE OwnerID = %s)
    """

def __count_rows():
        return """
            SELECT
            COUNT(Content)
            FROM blog_posts;
            """
def __read_post():
    return """
           SELECT
                u.Name,
                p.title,
                p.content,
                u.OwnerID,
                p.date,
                p.Date_modified
            FROM
                blog_users u
            INNER JOIN blog_posts p
                ON u.OwnerID = p.OwnerID
                where p.PostID = %s;
            """

def __read_all():
        return"""
            SELECT p.PostID,
            u.Name,
            p.Title,
            SUBSTRING(p.Content, 1, 150),
            p.OwnerID,
            p.Date
            FROM blog_posts p
            INNER JOIN blog_users u
            ON p.OwnerID = u.OwnerID 
            ORDER BY p.PostID DESC;

            """

def __read_user_posts():
        return """
            SELECT p.PostID,
                u.Name,
                p.Title,
                SUBSTRING(p.Content, 1, 150),
                p.OwnerID,
                p.Date
                FROM blog_posts p
            INNER JOIN blog_users u
                ON p.OwnerID = u.OwnerID
                AND p.OwnerID = %s
                ORDER BY p.PostID DESC;
            """

one_fetchable = ["get_by_mail", "get_by_id", "insert_user", "search", "read_post", "insert_post", "count_posts"]
all_fetchable = ["get_users", "get_user_posts", "get_inactive", "get_removed_posts", "read_all"]

def queries():
    return {
    "insert_user" : __insert_user(),
    "insert_post" : __insert_post(),
    "edit_user" : __update_user(),
    "edit_post" : __update_post(),
    "delete_user" : __delete_user(),
    "delete_post" : __delete_post(),
    "archive" : __archive(),
    "get_users" : __get_all_users(),
    "get_by_mail" : __get_user_by_identifier("Email"),
    "get_by_id" : __get_user_by_identifier("OwnerID"),
    "get_user_posts" : __read_user_posts(),
    "read_post" : __read_post(),
    "read_all" : __read_all(),
    "change_pass" : __change_password(),
    "search" : __has_user(),
    "get_inactive" : __get_removed_users(),
    "get_removed_posts" : __read_all_inactive(),
    "count_posts" : __count_rows()
    }

def fetch_if_needed(request, cursor):
        result = []
        if request in one_fetchable:
            result = cursor.fetchone()
        if request in all_fetchable:
            result = cursor.fetchall()
        return result