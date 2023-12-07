from protos import post_pb2
from protos import comment_pb2
from protos import user_pb2
from protos import post_pb2_grpc
from protos import subreddit_pb2

from datetime import datetime

class Post:
    """
    post object representing the common metadata between posts and videos
    """
    def __init__(self,DBConn,request):
        self.score = 0
        self.published=datetime.today().strftime('%m/%d/%Y')
        self.title = request.meta.title
        self.text = request.meta.text
        self.state = request.meta.state
        self.subreddit = DBConn.getSubreddit(request.meta.subreddit)
        self.ID = None
        self.tags = []

        # validate tags
        for tag in request.meta.tags:
                if tag in self.subreddit["tags"]:
                    self.tags.append(tag)

    def convertMeta(self):
        return post_pb2.PostMeta(
                ID=self.ID,
                title = self.title,
                text = self.text,
                state = self.state,
                published = self.published,
                score = self.score,
                subreddit = subreddit_pb2.Subreddit(
                    name = self.subreddit["name"],
                    state = self.subreddit["state"],
                    tags = self.subreddit["tags"]
                ),
                tags = self.tags
            )

class Image(Post):
    """
    image-specific class

    handles parsing database response and converting to a gRPC response
    """
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
        self.ID = DBConn.addNewImagePost(
            self.title,
            self.text,
            self.state,
            self.published,
            self.score,
            self.type,
            self.content,
            self.subreddit,
            self.tags
        )
    
class Video(Post):
    """
    video-specific class

    handles parsing database response and converting to a gRPC response
    """
    def __init__(self, DBConn, request):
        super().__init__(DBConn, request)
        self.type = "VIDEO"
        self.content = list(request.video.frames)

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
        self.ID = DBConn.addNewVideoPost(
            self.title,
            self.text,
            self.state,
            self.published,
            self.score,
            self.type,
            self.content,
            self.subreddit,
            self.tags
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

        # add to DB
        newImage.addNewImageToDatabase(self.DBConn)

        # make post response
        newImageResponse = newImage.convertToImagePostResponse()

        return newImageResponse

    def PostVideo(self, request, context):
        if not (request.meta.title and request.meta.text and request.meta.state):
            return post_pb2.newVideoResponse()

        if not request.video.frames:
            return post_pb2.newVideoResponse()

        # parse request
        newVideo = Video(self.DBConn,request)

        # add to DB
        newVideo.addNewVideoToDatabase(self.DBConn)
        
        # make post response
        newVideoResponse = newVideo.convertToVideoPostResponse()

        return newVideoResponse
    
    def GetPostContent(self, request, context):
        if request.postID == None:
            return post_pb2.GetPostContentResponse()
        
        # get post from DB
        post = self.DBConn.getPostByID(request.postID)

        if not post:
            return post_pb2.GetPostContentResponse()
        
        # first request is a type
        yield post_pb2.GetPostContentResponse(
            type=post["type"]
        )

        # further requests, send contents
        if post["type"] == "IMAGE":
            # one yield, return image url if image
            yield post_pb2.GetPostContentResponse(
                imageurl=post["content"]
            )
        elif post["type"] == "VIDEO":
            # if video, encapsulate each of videos frames in response
            for frame in post["content"]:
                yield post_pb2.GetPostContentResponse(
                    videoframe=frame
                )       
        else:
            return post_pb2.GetPostContentResponse()
        
    def RatePost(self, request, contex):
        if request.postID == None:
            return post_pb2.RatePostResponse()
        
        # get post from DB after changing the rating (upvote or downvote)
        post = self.DBConn.ratePost(request.postID, request.rating)

        if not post:
            return post_pb2.RatePostResponse()
        
        # prepare metadata response to send back to user
        RatePostResponse = post_pb2.RatePostResponse(
            meta=post_pb2.PostMeta(
                title = post["title"],
                text = post["text"],
                state = post["state"],
                published = post["published"],
                score = post["score"],
                ID = post["ID"],
                # subreddit = post["subreddit"],
                # tags = post["tags"]
            )
        )

        return RatePostResponse
    
    def GetPost(self, request, context):

        if request.postID == None:
            return post_pb2.GetPostMetaResponse()
        
        # get post by ID from DB
        post = self.DBConn.getPostByID(request.postID)

        if not post:
            return post_pb2.GetPostMetaResponse()

        # send post metadata response
        GetPostMetaResponse = post_pb2.GetPostMetaResponse(
            meta=post_pb2.PostMeta(
                title = post["title"],
                text = post["text"],
                state = post["state"],
                published = post["published"],
                score = post["score"],
                ID = post["ID"],
                subreddit = subreddit_pb2.Subreddit(
                    name=post["subreddit"]["name"],
                    state=post["subreddit"]["state"],
                    tags=post["subreddit"]["tags"],
                ),
                tags = post["tags"]
            )
        )

        return GetPostMetaResponse

    def GetNComments(self, request, context):

        if request.postID == None:
            return post_pb2.GetNCommentsResponse()
        
        # get post by ID from DB
        post = self.DBConn.getPostByID(request.postID)

        if not post:
            return post_pb2.GetNCommentsResponse()

        # sort the comments by order of score
        sorted_comments = sorted(post["comment"], key=lambda dict: -dict["score"])

        # enumerate all of the elements starting from highest score
        for i,comment in enumerate(sorted_comments):
            # while less than the requested number of comments
            if i < request.num_comments:

                # determine if comment has replies underneath it
                has_replies = (len(comment["comment"]) != 0)

                # send each comment one by one
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
            else:
                # break loop after N comments
                break

    def MonitorPostScore(self, request_iterator, context):

        monitored = {}

        # get the FIRST request - should be a postID
        request = request_iterator.next()
        postID = request.postID

        # get post by ID from DB
        post = self.DBConn.getPostByID(postID)
        
        if not post:
            return post_pb2.MonitorScoreResponse()

        # return a post score first
        yield post_pb2.MonitorScoreResponse(
            postID=postID,
            postScore=post["score"]
        )
        
        # now store known comments in here
        commentIDs = []

        for request in request_iterator:
            # continue polling DB
            post = self.DBConn.getPostByID(postID)

            if not post:
                return post_pb2.MonitorScoreResponse()

            # add new comment ID if possible
            if request.commentID not in commentIDs:
                if(self.DBConn.getCommentByID(request.commentID)):
                    commentIDs.append(request.commentID)
            
            # iterate available commentIDs
            commentScores = []

            for commentID in commentIDs:
                comment = self.DBConn.getCommentByID(commentID)
                commentScores.append(comment["score"])

            yield post_pb2.MonitorScoreResponse(
                postID=postID,
                postScore=post["score"],
                commentIDs=commentIDs,
                commentScores=commentScores,
            )