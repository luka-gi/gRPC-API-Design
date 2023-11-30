import grpc
import post_pb2_grpc
import post_pb2
import comment_pb2_grpc
import comment_pb2
import user_pb2

class client_gRPC_API:

    def __init__(self,client_config):
        self.port = client_config.port
        self.host = client_config.host
        self.channel = None
        self.post_service = None
        self.comment_service = None

    def open(self):
        server_location = self.host + ":" + self.port

        self.channel = grpc.insecure_channel(server_location)

        self.post_service = post_pb2_grpc.PostServiceStub(self.channel)
        self.comment_service = comment_pb2_grpc.CommentServiceStub(self.channel)

    def postImage(self, title, text, state, image_url):
        return self.post_service.PostImage(post_pb2.NewImagePostRequest(
            meta=post_pb2.NewPostMeta(
                title=title,
                text=text,
                state=state,
            ),
            image=post_pb2.Image(url=image_url)
        ))
    
    def postVideo(self, title, text, state, video_frames):
        return self.post_service.PostVideo(post_pb2.NewVideoPostRequest(
            meta=post_pb2.NewPostMeta(
                title=title,
                text=text,
                state=state,
            ),
            video=post_pb2.Video(frames=video_frames)
        ))
    
    def getPostContent(self, postID):
        response = self.post_service.GetPostContent(post_pb2.GetPostContentRequest(
            postID=postID
        ))

        response_list = list(response)

        type = response_list[0].type

        if type == post_pb2.PostMeta(type="IMAGE").type:
            return response_list[1].imageurl
        elif type == post_pb2.PostMeta(type="VIDEO").type:
            return response_list[1].videoframes
        else:
            return None
        
    def ratePost(self, postID, rating):
        response = self.post_service.RatePost(post_pb2.RatePostRequest(
            postID=postID,
            rating=rating
        ))

        return response

    def close(self):
        self.channel.close()

    def createComment(self, userID, content, state):
        return self.comment_service.CreateComment(comment_pb2.NewCommentRequest(
            author=user_pb2.User(
                UID = userID
            ),
            state = state,
            content=content
        ))
    
    def rateComment(self, commentID, rating):
        response = self.comment_service.RateComment(comment_pb2.RateCommentRequest(
            commentID=commentID,
            rating=rating
        ))

        return response
    
    def getNComments(self, commentID, numComments):
        response = self.comment_service.GetNComments(comment_pb2.GetNCommentsRequest(
            commentID=commentID,
            num_comments=numComments
        ))

        return response