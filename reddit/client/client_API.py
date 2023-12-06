import grpc
import sys

sys.path.append("protos")
from protos import post_pb2_grpc
from protos import post_pb2
from protos import comment_pb2_grpc
from protos import comment_pb2
from protos import user_pb2

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
        
        if (title == None or text == None or image_url == None):
            return None

        response = self.post_service.PostImage(post_pb2.NewImagePostRequest(
            meta=post_pb2.NewPostMeta(
                title=title,
                text=text,
                state=state,
            ),
            image=post_pb2.Image(url=image_url)
        ))

        responseToDict = {
            "title":response.meta.title,
            "text":response.meta.text,
            "score":response.meta.score,
            "state":response.meta.state,
            "published":response.meta.published,
            "ID":response.meta.ID,
            "type":response.meta.type,
            "comment":response.meta.comment,
            "content":response.image.url,
        }

        return responseToDict
    
    def postVideo(self, title, text, state, video_frames):

        if (title == None or text == None or video_frames == None):
            return None

        if (len(video_frames) == 0):
            return None

        response = self.post_service.PostVideo(post_pb2.NewVideoPostRequest(
            meta=post_pb2.NewPostMeta(
                title=title,
                text=text,
                state=state,
            ),
            video=post_pb2.Video(frames=video_frames)
        ))
    
        responseToDict = {
            "title":response.meta.title,
            "text":response.meta.text,
            "score":response.meta.score,
            "state":response.meta.state,
            "published":response.meta.published,
            "ID":response.meta.ID,
            "type":response.meta.type,
            "comment":response.meta.comment,
            "content":response.video.frames,
        }

        return responseToDict
    
    def getPostMeta(self, postID):
        response = self.post_service.GetPost(post_pb2.GetPostMetaRequest(
            postID=postID
        ))

        if (response == post_pb2.GetPostMetaResponse()):
            return None

        responseToDict = {
            "title":response.meta.title,
            "text":response.meta.text,
            "score":response.meta.score,
            "state":response.meta.state,
            "published":response.meta.published,
            "ID":response.meta.ID,
            "type":response.meta.type,
        }

        return responseToDict
    
    def getPostContent(self, postID):
        response = self.post_service.GetPostContent(post_pb2.GetPostContentRequest(
            postID=postID
        ))

        response_list = list(response)

        if len(response_list) == 0:
            return None

        type = response_list[0].type
        content_list = response_list[1:]

        if type == post_pb2.PostMeta(type="IMAGE").type:
            return content_list[0].imageurl
        elif type == post_pb2.PostMeta(type="VIDEO").type:
            return [content_list[x].videoframe for x in range(len(content_list))]
        else:
            return None
        
    def ratePost(self, postID, rating):
        response = self.post_service.RatePost(post_pb2.RatePostRequest(
            postID=postID,
            rating=rating
        ))

        if response == post_pb2.RatePostResponse():
            return None

        return response.meta.score

    def close(self):
        self.channel.close()

    def createComment(self, userID, content, state):

        if (userID == None or content == None):
            return None

        response = self.comment_service.CreateComment(comment_pb2.NewCommentRequest(
            author=user_pb2.User(
                UID = userID
            ),
            state = state,
            content=content
        ))
    
        responseToDict = {
            "author":response.comment.author.UID,
            "score":response.comment.score,
            "state":response.comment.state,
            "published":response.comment.published,
            "content":response.comment.content,
            "ID":response.comment.ID,
            "comment":response.comment.comment,
        }

        return responseToDict
    
    def rateComment(self, commentID, rating):
        response = self.comment_service.RateComment(comment_pb2.RateCommentRequest(
            commentID=commentID,
            rating=rating
        ))

        if(response == comment_pb2.RateCommentResponse()):
            return None

        return response.comment.score
    
    def getComment(self, commentID):
        response = self.comment_service.GetComment(comment_pb2.GetCommentRequest(
            commentID=commentID
        ))

        if(response == comment_pb2.GetCommentResponse()):
            return None
    
        responseToDict = {
            "author":response.comment.author.UID,
            "score":response.comment.score,
            "state":response.comment.state,
            "published":response.comment.published,
            "content":response.comment.content,
            "ID":response.comment.ID,
        }

        return responseToDict
    
    def getNCommentsFromComment(self, commentID, numComments):
        responses = self.comment_service.GetNComments(comment_pb2.GetNCommentsRequest(
            commentID=commentID,
            num_comments=numComments
        ))

        toReturn = []
        responses = list(responses)

        for response in responses:
            comment_object = {}

            if response.comment != comment_pb2.Comment():
                comment_object["author"] = response.comment.author.UID
                comment_object["score"] = response.comment.score
                comment_object["state"] = response.comment.state
                comment_object["published"] = response.comment.published
                comment_object["content"] = response.comment.content
                comment_object["ID"] = response.comment.ID
                comment_object["comment"] = []

                toReturn.append(comment_object)

            if response.subcomment != comment_pb2.Comment():
                comment_object["author"] = response.subcomment.author.UID
                comment_object["score"] = response.subcomment.score
                comment_object["state"] = response.subcomment.state
                comment_object["published"] = response.subcomment.published
                comment_object["content"] = response.subcomment.content
                comment_object["ID"] = response.subcomment.ID
                comment_object["comment"] = []

                toReturn[-1]["comment"].append(comment_object)

        return toReturn
    
    def getNCommentsFromPost(self, postID, numComments):
        responses = self.post_service.GetNComments(post_pb2.GetNCommentsRequest(
            postID=postID,
            num_comments=numComments
        ))

        toReturn = []

        for response in list(responses):
            comment_object = {}
            
            comment_object["author"] = response.comment.author.UID
            comment_object["score"] = response.comment.score
            comment_object["state"] = response.comment.state
            comment_object["published"] = response.comment.published
            comment_object["content"] = response.comment.content
            comment_object["ID"] = response.comment.ID
            comment_object["has_replies"] = response.has_replies

            toReturn.append(comment_object)

        return toReturn