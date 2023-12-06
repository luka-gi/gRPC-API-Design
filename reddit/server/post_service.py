from protos import post_pb2
from protos import comment_pb2
from protos import user_pb2
from protos import post_pb2_grpc

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

    def __init__(self, DBConn):
        super().__init__()
        self.DBConn = DBConn

    def PostImage(self, request, context):
        if not (request.meta.title and request.meta.text and request.meta.state):
            return post_pb2.newImageResponse()

        if not request.image.url:
            return post_pb2.newImageResponse()
        
        # parse request
        newImage = Image(self.DBConn,request)

        # make post response
        newImageResponse = newImage.convertToImagePostResponse()

        # add to DB
        newImage.addNewImageToDatabase(self.DBConn)

        return newImageResponse

    def PostVideo(self, request, context):
        if not (request.meta.title and request.meta.text and request.meta.state):
            return post_pb2.newVideoResponse()

        if not request.video.frames:
            return post_pb2.newVideoResponse()

        # parse request
        newVideo = Video(self.DBConn,request)

        # make post response
        newVideoResponse = newVideo.convertToVideoPostResponse()

        # add to DB
        newVideo.addNewVideoToDatabase(self.DBConn)

        return newVideoResponse
    
    def GetPostContent(self, request, context):
        if request.postID == None:
            return post_pb2.GetPostContentResponse()
        
        post = self.DBConn.getPostByID(request.postID)

        if not post:
            return post_pb2.GetPostContentResponse()
        
        yield post_pb2.GetPostContentResponse(
            type=post["type"]
        )

        if post["type"] == "IMAGE":
            yield post_pb2.GetPostContentResponse(
                imageurl=post["content"]
            )
        elif post["type"] == "VIDEO":
            for frame in post["content"]:
                yield post_pb2.GetPostContentResponse(
                    videoframe=frame
                )       
        else:
            return post_pb2.GetPostContentResponse()
        
    def RatePost(self, request, contex):
        if request.postID == None:
            return post_pb2.RatePostResponse()
        
        post = self.DBConn.ratePost(request.postID, request.rating)

        if not post:
            return post_pb2.RatePostResponse()
        
        RatePostResponse = post_pb2.RatePostResponse(
            meta=post_pb2.PostMeta(
                title = post["title"],
                text = post["text"],
                state = post["state"],
                published = post["published"],
                score = post["score"],
                ID = post["ID"]
            )
        )

        return RatePostResponse
    
    def GetPost(self, request, context):

        if request.postID == None:
            return post_pb2.GetPostMetaResponse()
        # add comment to DB
        post = self.DBConn.getPostByID(request.postID)

        if not post:
            return post_pb2.GetPostMetaResponse()

        GetPostMetaResponse = post_pb2.GetPostMetaResponse(
            meta=post_pb2.PostMeta(
                title = post["title"],
                text = post["text"],
                state = post["state"],
                published = post["published"],
                score = post["score"],
                ID = post["ID"]
            )
        )

        return GetPostMetaResponse

    def GetNComments(self, request, context):

        if request.postID == None:
            return post_pb2.GetNCommentsResponse()
        
        post = self.DBConn.getPostByID(request.postID)

        if not post:
            return post_pb2.GetNCommentsResponse()

        sorted_comments = sorted(post["comment"], key=lambda dict: -dict["score"])

        for i,comment in enumerate(sorted_comments):
            if i < request.num_comments:

                has_replies = (len(comment["comment"]) != 0)

                yield post_pb2.GetNCommentsResponse(
                    comment=comment_pb2.Comment(
                        score = comment["score"],
                        published = comment["published"],
                        content = comment["content"],
                        state = comment["state"],
                        ID = comment["ID"],
                        author = user_pb2.User(
                            UID=comment["author"],
                        ),
                    ),
                    has_replies=has_replies
                )
