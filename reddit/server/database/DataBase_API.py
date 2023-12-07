"""
implemented API used for abstracting the DB implementation from the requested/returned data
as well as how to change or add the items in the database 
"""
from database.DataBase import database_in_mem
import sqlite3
import json

class DataBase():
    def __init__(self):
        pass

    def connect(self):
        return self
    
    def close(self):
        pass

    def _close_sqlite(self,connection,cursor):
        cursor.close()
        connection.close()

    def _to_dict(self,cursor, row):
        dict = {}
        for idx, col in enumerate(cursor.description):
            dict[col[0]] = row[idx]
        return dict
    
    def _connect_sqlite(self):
        connection = sqlite3.connect("database/reddit.db")
        connection.row_factory = self._to_dict
        cursor = connection.cursor()

        return (connection,cursor)

    def getNewPostID(self):
        pre_increment = database_in_mem.PostID

        database_in_mem.PostID = database_in_mem.PostID + 1

        return pre_increment
    
    def addNewImagePost(self, title, text, state, published, score, ID, type, content, subreddit, tags):
        (connection, cursor) = self._connect_sqlite()
        
        input = {
            "score": score,
            "published": published,
            "ID": ID,
            "title": title,
            "text": text,
            "state": state,
            "type": type,
            "content": content,
            "comment": "[]",
            "subreddit": json.dumps(subreddit),
            "tags": json.dumps(tags)
        }

        cursor.execute('''INSERT INTO
            posts
            (
                title,
                text,
                score,
                state,
                published,
                ID,
                type,
                content,
                comment,
                subreddit,
                tags
            )
            VALUES
            (
                :title,
                :text,
                :score,
                :state,
                :published,
                :ID,
                :type,
                :content,
                :comment,
                :subreddit,
                :tags
            )
            ''',input)

        connection.commit()
        self._close_sqlite(connection,cursor)


    def addNewVideoPost(self, title, text, state, published, score, ID, types, content, subreddit, tags):
        (connection, cursor) = self._connect_sqlite()

        input = {
            "score": score,
            "published": published,
            "ID": ID,
            "title": title,
            "text": text,
            "state": state,
            "type": types,
            "content": json.dumps(content),
            "comment": "[]",
            "subreddit": json.dumps(subreddit),
            "tags": json.dumps(tags)
        }

        cursor.execute('''INSERT INTO
            posts
            (
                title,
                text,
                score,
                state,
                published,
                ID,
                type,
                content,
                comment,
                subreddit,
                tags
            )
            VALUES
            (
                :title,
                :text,
                :score,
                :state,
                :published,
                :ID,
                :type,
                :content,
                :comment,
                :subreddit,
                :tags
            )
            ''',input)

        connection.commit()
        self._close_sqlite(connection,cursor)

    def getPosts(self):
        (connection, cursor) = self._connect_sqlite()
        cursor.execute('SELECT * FROM posts')
        posts = cursor.fetchall()

        # arrays and objects, such as videoframes and subreddits, need to be re-parsed
        for post in posts:
            post["content"] = json.loads(post["content"])
            post["subreddit"] = json.loads(post["subreddit"])
            post["tags"] = json.loads(post["tags"])

        self._close_sqlite(connection, cursor)

        return posts
    
    def getPostByID(self, postID):
        (connection, cursor) = self._connect_sqlite()
        cursor.execute('SELECT * FROM posts WHERE ID={}'.format(postID))
        post = cursor.fetchone()

        if not post:
            self._close_sqlite(connection, cursor)
            return None

        # arrays and objects, such as videoframes and subreddits, need to be re-parsed
        post["comment"] = json.loads(post["comment"])
        post["content"] = json.loads(post["content"])
        post["subreddit"] = json.loads(post["subreddit"])
        post["tags"] = json.loads(post["tags"])

        self._close_sqlite(connection, cursor)

        return post
    
    def ratePost(self, postID, rating):
        (connection, cursor) = self._connect_sqlite()

        post = None

        if(rating == "UPVOTE"):
            cursor.execute('UPDATE posts SET score=score+1 WHERE ID={} RETURNING *'.format(postID))
            post = cursor.fetchone()

        elif(rating == "DOWNVOTE"):
            cursor.execute('UPDATE posts SET score=score-1 WHERE ID={} RETURNING *'.format(postID))
            post = cursor.fetchone()

        if not post:
            self._close_sqlite(connection, cursor)
            return None

        connection.commit()
        self._close_sqlite(connection, cursor)

        return post
    
    def getNewCommentID(self):
        pre_increment = database_in_mem.CommentID

        database_in_mem.CommentID = database_in_mem.CommentID + 1

        return pre_increment
    
    def addNewComment(self, score, published, state, content, ID, author):

        (connection, cursor) = self._connect_sqlite()
        
        input = {
            "ID": ID,
            "score": score,
            "author": author,
            "state": state,
            "published": published,
            "content": content,
            "comment": "[]",
        }

        cursor.execute('''INSERT INTO
        comments
        (
            ID,
            score,
            author,
            state,
            published,
            content,
            comment
        )
        VALUES
        (
            :ID,
            :score,
            :author,
            :state,
            :published,
            :content,
            :comment
        )
        ''',input)

        connection.commit()
        self._close_sqlite(connection,cursor)
    
    def getCommentByID(self, commentID):
        (connection, cursor) = self._connect_sqlite()
        cursor.execute('SELECT * FROM comments WHERE ID={}'.format(commentID))
        comment = cursor.fetchone()

        if not comment:
            self._close_sqlite(connection, cursor)
            return None

        # arrays and objects, such as videoframes and subreddits, need to be re-parsed
        comment["comment"] = json.loads(comment["comment"])

        self._close_sqlite(connection, cursor)

        return comment
    
    def rateComment(self, commentID, rating):
        (connection, cursor) = self._connect_sqlite()

        comment = None

        if(rating == "UPVOTE"):
            cursor.execute('UPDATE comments SET score=score+1 WHERE ID={} RETURNING *'.format(commentID))
            comment = cursor.fetchone()

        elif(rating == "DOWNVOTE"):
            cursor.execute('UPDATE comments SET score=score-1 WHERE ID={} RETURNING *'.format(commentID))
            comment = cursor.fetchone()

        if not comment:
            self._close_sqlite(connection, cursor)
            return None

        connection.commit()
        self._close_sqlite(connection, cursor)

        return comment

    def getSubreddit(self, name):
        (connection, cursor) = self._connect_sqlite()
        cursor.execute('SELECT * FROM subreddits WHERE name="{}"'.format(name))
        subreddit = cursor.fetchone()

        if not subreddit:
            return None

        # arrays and objects, such as videoframes and subreddits, need to be re-parsed
        subreddit["tags"] = json.loads(subreddit["tags"])

        self._close_sqlite(connection, cursor)

        return subreddit
    
    def getSubredditTags(self, name):
        subreddit = self.getSubreddit(name)

        if(subreddit):
            return subreddit["tags"]
        else:
            return None

# class DataBase_InMem():
#     def __init__(self):
#         self.connection = None

#     def connect(self):
#         return self

#     def close(self):
#         pass

#     def getNewPostID(self):
#         pre_increment = database_in_mem.PostID

#         database_in_mem.PostID = database_in_mem.PostID + 1

#         return pre_increment
    
#     def addNewImagePost(self, title, text, state, published, score, ID, type, content, comment, subreddit, tags):
#         database_in_mem.Posts.append({
#             "score": score,
#             "published": published,
#             "ID": ID,
#             "title": title,
#             "text": text,
#             "state": state,
#             "type": type,
#             "content": content,
#             "comment": comment,
#             "subreddit": subreddit,
#             "tags": tags
#         })

#     def addNewVideoPost(self, title, text, state, published, score, ID, type, content, comment, subreddit, tags):
#         database_in_mem.Posts.append({
#             "score": score,
#             "published": published,
#             "ID": ID,
#             "title": title,
#             "text": text,
#             "state": state,
#             "type": type,
#             "content": content,
#             "comment": comment,
#             "subreddit": subreddit,
#             "tags": tags
#         })

#     def getPosts(self):
#         return database_in_mem.Posts
    
#     def getPostByID(self, postID):
#         for post in database_in_mem.Posts:
#             if post["ID"] is postID:
#                 return post
#         return None
    
#     def ratePost(self, postID, rating):
#         post = self.getPostByID(postID)

#         if not post:
#             return None

#         if(rating == "UPVOTE"):
#             post["score"] = post["score"] + 1
#         elif(rating == "DOWNVOTE"):
#             post["score"] = post["score"] - 1

#         return post
    
#     def getNewCommentID(self):
#         pre_increment = database_in_mem.CommentID

#         database_in_mem.CommentID = database_in_mem.CommentID + 1

#         return pre_increment
    
#     def addNewComment(self, score, published, state, content, ID, author):
#         database_in_mem.Comments.append({
#             "score":score,
#             "published":published,
#             "state":state,
#             "content":content,
#             "ID":ID,
#             "author":author
#         })

#     def getComments(self):
#         return database_in_mem.Comments
    
#     def getCommentByID(self, commentID):
#         for comment in database_in_mem.Comments:
#             if comment["ID"] is commentID:
#                 return comment
#         return None
    
#     def rateComment(self, commentID, rating):
#         comment = self.getCommentByID(commentID)

#         if not comment:
#             return None

#         if(rating == "UPVOTE"):
#             comment["score"] = comment["score"] + 1
#         elif(rating == "DOWNVOTE"):
#             comment["score"] = comment["score"] - 1

#         return comment

#     def getSubreddit(self, name):
#         for subreddit in database_in_mem.SubReddits:
#             if subreddit["name"] == name:
#                 return subreddit
#         return None
    
#     def getSubredditTags(self, name):
#         subreddit = self.getSubreddit(name)

#         if(subreddit):
#             return subreddit.tags
#         else:
#             return None
        