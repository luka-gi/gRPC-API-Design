from database.DataBase import database_in_mem

class DataBase():
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
    
    def addNewImagePost(self, title, text, state, published, score, ID, type, content):
        database_in_mem.Posts.append({
            "score": score,
            "published": published,
            "ID": ID,
            "title": title,
            "text": text,
            "state": state,
            "type": type,
            "content": content,
        })

    def addNewVideoPost(self, title, text, state, published, score, ID, type, content):
        database_in_mem.Posts.append({
            "score": score,
            "published": published,
            "ID": ID,
            "title": title,
            "text": text,
            "state": state,
            "type": type,
            "content": content,
        })

    def getPosts(self):
        return database_in_mem.Posts