

def get_queries():
    return [
        (
        "SET client_encoding = 'UTF8';",
        """      
            CREATE TABLE IF NOT EXISTS blog_users(
            OwnerID SERIAL PRIMARY KEY,
            Name varchar(30),
            Email varchar(200),
            Password varchar(5000),
            Date varchar(50),
            Date_modified varchar(50));
        """,
            """        
            CREATE TABLE IF NOT EXISTS blog_posts(
            PostID SERIAL PRIMARY KEY,
            OwnerID int,
            Title varchar(200),
            Content varchar(5000),
            Date varchar(50),
            Date_modified varchar(50),
            CONSTRAINT fk_owner
            FOREIGN KEY(OwnerID) 
            REFERENCES blog_users(OwnerID)
            ON DELETE CASCADE
            ON UPDATE CASCADE);
        """,
        """
            ALTER TABLE blog_posts
            ADD Column IF NOT EXISTS
            OwnerID int;
        """,
        """
            DO $$
            BEGIN
                if not exists(select * from information_schema.key_column_usage
                    where constraint_catalog=current_catalog
                    and table_name='blog_posts'
                    and constraint_name = 'owner_fk'
                    and position_in_unique_constraint notnull)
                then
                    execute 
                        'ALTER TABLE blog_posts
                        ADD CONSTRAINT owner_fk 
                        FOREIGN KEY (OwnerID)
                        REFERENCES blog_users(OwnerID)
                        ON DELETE CASCADE
                        ON UPDATE CASCADE';
                end if;
            end;
            $$
            LANGUAGE plpgsql;
        """),
        ("""        
            CREATE TABLE IF NOT EXISTS deleted_users(
            Email varchar(200),
            Content varchar(5000),
            deleted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP);
        """,
        """ 
           CREATE OR REPLACE FUNCTION delete_expired_archived() RETURNS trigger
            LANGUAGE plpgsql
        AS $$
        BEGIN
        DELETE FROM deleted_users WHERE deleted_at < NOW() - interval '1 year';
        RETURN NEW;
        END;
        $$;
            DROP TRIGGER IF EXISTS expired_users_delete
            ON public.deleted_users;
            CREATE TRIGGER expired_users_delete
            AFTER INSERT ON deleted_users
            EXECUTE PROCEDURE delete_expired_archived();
        """),      
        ("""    
            do $$
            declare
                first_row record;
                pass text := %s;
                creation_date text := %s;
            begin
                SELECT *
                into first_row
                FROM blog_users
                LIMIT 1;

                IF first_row IS NULL THEN

                    INSERT INTO blog_users
                    VALUES(DEFAULT, 'Admin1', 'default@admin', pass, creation_date);
                
                ELSIF first_row.Email <> 'default@admin' THEN

                    INSERT INTO blog_users
                    VALUES(1, 'Admin1', 'default@admin', pass, creation_date) 
                    ON CONFLICT ON CONSTRAINT blog_users_pkey
                    DO 
                    UPDATE SET NAME = 'Admin1', Email = 'default@admin', Password = pass, Date = creation_date;

                    INSERT INTO blog_users
                    VALUES(DEFAULT, first_row.NAME, first_row.Email, first_row.Password, first_row.Date, first_row.Date_modified);
                END IF;
            END;
            $$
            LANGUAGE plpgsql;
        """,),        
        ("""
           DO $$
                declare
                    mail text := '@dummy.com';
            BEGIN
                if exists(SELECT *
                    FROM information_schema.columns 
                    WHERE table_schema='public' AND
                    table_name='blog_posts' AND
                    column_name='author')
                then      
                    INSERT INTO blog_users (Name, Email, Password)
                    SELECT Author, Author || mail, Author
                    FROM blog_posts
                    WHERE blog_posts.OwnerID is Null;

                    UPDATE blog_posts
                    SET OwnerID = blog_users.OwnerID
                    FROM blog_users
                    WHERE blog_posts.OwnerID is NULL AND
                    blog_users.Email = blog_posts.Author || mail; 
            
                    ALTER table blog_posts
                    DROP COLUMN
                    Author;     
            
            end if;
        end;
        $$
        LANGUAGE plpgsql;
        """,)]

