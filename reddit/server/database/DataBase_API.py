from database.DataBase import database_in_mem

class DataBase():
    def __init__(self):
        self.connection = None

    def connect(self):
        pass

    def close(self):
        pass

    def getNewPostID(self):
        pre_increment = database_in_mem.PostID

        database_in_mem.PostID = database_in_mem.PostID + 1

        return pre_increment
    
    def addNewImagePost(self, title, text, state, published, score, ID, type, content):
        pass