import post_pb2
import post_pb2_grpc

from database.DataBase import database_in_mem
from database.DataBase_API import DataBase
from datetime import datetime

class Post:
    def __init__(self,DBConn,request):
        self.score = 0
        self.published=datetime.today().strftime('%m/%d/%Y')
        self.title = request.meta.title
        self.text = request.meta.text
        self.state = request.meta.state
        self.ID = DBConn.getNewPostID()

    def convertMeta(self):
        return post_pb2.PostMeta(
                title = self.title,
                text = self.text,
                state = self.state,
                published = self.published,
                score = self.score,
                ID = self.ID
            )

class Image(Post):
    def __init__(self, DBConn, request):
        super().__init__(DBConn, request)
        self.type = "IMAGE"
        self.content = request.image.url

    def convertMeta(self):
        MetaToReturn = super().convertMeta()
        MetaToReturn.type = self.type
        return MetaToReturn

    def convertImage(self):
        return post_pb2.Image(
            url = self.content
        )

    def convertToImagePostResponse(self):
        return post_pb2.ImagePostResponse(
            meta=self.convertMeta(),
            image=self.convertImage()
        )
    
    def addNewImageToDatabase(self, DBConn):
        DBConn.addNewImagePost(
            self.title,
            self.text,
            self.state,
            self.published,
            self.score,
            self.ID,
            self.type,
            self.content
        )
    
class Video(Post):
    def __init__(self, DBConn, request):
        super().__init__(DBConn, request)
        self.type = "VIDEO"
        self.content = request.video.frames

    def convertMeta(self):
        MetaToReturn = super().convertMeta()
        MetaToReturn.type = self.type
        return MetaToReturn

    def convertVideo(self):
        return post_pb2.Video(
            frames = self.content
        )

    def convertToVideoPostResponse(self):
        return post_pb2.VideoPostResponse(
            meta=self.convertMeta(),
            video=self.convertVideo()
        )
    
    def addNewVideoToDatabase(self, DBConn):
        DBConn.addNewImagePost(
            self.title,
            self.text,
            self.state,
            self.published,
            self.score,
            self.ID,
            self.type,
            self.content
        )

class Poster(post_pb2_grpc.PostServiceServicer):

    def __init__(self):
        super().__init__()
        self.DBConn = DataBase()

    def requestValidated(self,request):
        if not (request.meta.title and request.meta.text and request.meta.state):
            return False

        return True

    def PostImage(self, request, context):
        if not self.requestValidated(request):
            return None

        if not request.image.url:
            return None
        
        # parse request
        newImage = Image(self.DBConn,request)

        # make post response
        newImageResponse = newImage.convertToImagePostResponse()

        # add to DB
        newImage.addNewImageToDatabase(self.DBConn)

        print(database_in_mem.Posts)

        return newImageResponse

    def PostVideo(self, request, context):
        if not self.requestValidated(request):
            return None

        if not request.video.frames:
            return None

        # parse request
        newVideo = Video(self.DBConn,request)

        # make post response
        newVideoResponse = newVideo.convertToVideoPostResponse()

        # add to DB
        newVideo.addNewVideoToDatabase(self.DBConn)

        print(database_in_mem.Posts)

        return newVideoResponse