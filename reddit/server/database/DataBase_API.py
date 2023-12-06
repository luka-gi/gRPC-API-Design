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

    def _connect_sqlite(self):
        connection = sqlite3.connect("database/reddit.db")
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
        return database_in_mem.Posts
    
    def getPostByID(self, postID):
        for post in database_in_mem.Posts:
            if post["ID"] is postID:
                return post
        return None
    
    def ratePost(self, postID, rating):
        post = self.getPostByID(postID)

        if not post:
            return None

        if(rating == "UPVOTE"):
            post["score"] = post["score"] + 1
        elif(rating == "DOWNVOTE"):
            post["score"] = post["score"] - 1

        return post
    
    def getNewCommentID(self):
        pre_increment = database_in_mem.CommentID

        database_in_mem.CommentID = database_in_mem.CommentID + 1

        return pre_increment
    
    def addNewComment(self, score, published, state, content, ID, author):
        database_in_mem.Comments.append({
            "score":score,
            "published":published,
            "state":state,
            "content":content,
            "ID":ID,
            "author":author
        })

    def getComments(self):
        return database_in_mem.Comments
    
    def getCommentByID(self, commentID):
        for comment in database_in_mem.Comments:
            if comment["ID"] is commentID:
                return comment
        return None
    
    def rateComment(self, commentID, rating):
        comment = self.getCommentByID(commentID)

        if not comment:
            return None

        if(rating == "UPVOTE"):
            comment["score"] = comment["score"] + 1
        elif(rating == "DOWNVOTE"):
            comment["score"] = comment["score"] - 1

        return comment

    def getSubreddit(self, name):
        for subreddit in database_in_mem.SubReddits:
            if subreddit["name"] == name:
                return subreddit
        return None
    
    def getSubredditTags(self, name):
        subreddit = self.getSubreddit(name)

        if(subreddit):
            return subreddit.tags
        else:
            return None

class DataBase_InMem():
    def __init__(self):
        self.connection = None

    def connect(self):
        return self

    def close(self):
        pass

    def getNewPostID(self):
        pre_increment = database_in_mem.PostID

        database_in_mem.PostID = database_in_mem.PostID + 1

        return pre_increment
    
    def addNewImagePost(self, title, text, state, published, score, ID, type, content, comment, subreddit, tags):
        database_in_mem.Posts.append({
            "score": score,
            "published": published,
            "ID": ID,
            "title": title,
            "text": text,
            "state": state,
            "type": type,
            "content": content,
            "comment": comment,
            "subreddit": subreddit,
            "tags": tags
        })

    def addNewVideoPost(self, title, text, state, published, score, ID, type, content, comment, subreddit, tags):
        database_in_mem.Posts.append({
            "score": score,
            "published": published,
            "ID": ID,
            "title": title,
            "text": text,
            "state": state,
            "type": type,
            "content": content,
            "comment": comment,
            "subreddit": subreddit,
            "tags": tags
        })

    def getPosts(self):
        return database_in_mem.Posts
    
    def getPostByID(self, postID):
        for post in database_in_mem.Posts:
            if post["ID"] is postID:
                return post
        return None
    
    def ratePost(self, postID, rating):
        post = self.getPostByID(postID)

        if not post:
            return None

        if(rating == "UPVOTE"):
            post["score"] = post["score"] + 1
        elif(rating == "DOWNVOTE"):
            post["score"] = post["score"] - 1

        return post
    
    def getNewCommentID(self):
        pre_increment = database_in_mem.CommentID

        database_in_mem.CommentID = database_in_mem.CommentID + 1

        return pre_increment
    
    def addNewComment(self, score, published, state, content, ID, author):
        database_in_mem.Comments.append({
            "score":score,
            "published":published,
            "state":state,
            "content":content,
            "ID":ID,
            "author":author
        })

    def getComments(self):
        return database_in_mem.Comments
    
    def getCommentByID(self, commentID):
        for comment in database_in_mem.Comments:
            if comment["ID"] is commentID:
                return comment
        return None
    
    def rateComment(self, commentID, rating):
        comment = self.getCommentByID(commentID)

        if not comment:
            return None

        if(rating == "UPVOTE"):
            comment["score"] = comment["score"] + 1
        elif(rating == "DOWNVOTE"):
            comment["score"] = comment["score"] - 1

        return comment

    def getSubreddit(self, name):
        for subreddit in database_in_mem.SubReddits:
            if subreddit["name"] == name:
                return subreddit
        return None
    
    def getSubredditTags(self, name):
        subreddit = self.getSubreddit(name)

        if(subreddit):
            return subreddit.tags
        else:
            return None