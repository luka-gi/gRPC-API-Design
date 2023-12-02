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

    def postImage(self, title, text, state, image_url, subreddit, tags):
        
        if (title == None or text == None or image_url == None or subreddit == None or tags == None):
            return None

        # send a title, a description, an initial state, and an image url
        response = self.post_service.PostImage(post_pb2.NewImagePostRequest(
            meta=post_pb2.NewPostMeta(
                title=title,
                text=text,
                state=state,
                subreddit=subreddit,
                tags=tags
            ),
            image=post_pb2.Image(url=image_url)
        ))

        # convert post response to python dictionary
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
            "subreddit":{
                "name":response.meta.subreddit.name,
                "state":response.meta.subreddit.state,
                "tags":response.meta.subreddit.tags,
            },
            "tags":response.meta.tags,
        }

        return responseToDict
    
    def postVideo(self, title, text, state, video_frames, subreddit, tags):

        if (title == None or text == None or video_frames == None or subreddit == None or tags == None):
            return None

        if (len(video_frames) == 0):
            return None

        # send a title, a description, an initial state, and a list of videoframes
        response = self.post_service.PostVideo(post_pb2.NewVideoPostRequest(
            meta=post_pb2.NewPostMeta(
                title=title,
                text=text,
                state=state,
                subreddit=subreddit,
                tags=tags
            ),
            video=post_pb2.Video(frames=video_frames)
        ))
    
        # convert post response to python dictionary
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
            "subreddit":{
                "name":response.meta.subreddit.name,
                "state":response.meta.subreddit.state,
                "tags":response.meta.subreddit.tags,
            },
            "tags":response.meta.tags,
        }

        return responseToDict
    
    def getPostMeta(self, postID):
        # send a post ID to get metadata from
        response = self.post_service.GetPost(post_pb2.GetPostMetaRequest(
            postID=postID
        ))

        if (response == post_pb2.GetPostMetaResponse()):
            return None

        # convert response to python dictionary
        responseToDict = {
            "title":response.meta.title,
            "text":response.meta.text,
            "score":response.meta.score,
            "state":response.meta.state,
            "published":response.meta.published,
            "ID":response.meta.ID,
            "type":response.meta.type,
            "subreddit":{
                "name":response.meta.subreddit.name,
                "state":response.meta.subreddit.state,
                "tags":response.meta.subreddit.tags,
            },
            "tags":response.meta.tags,
        }

        return responseToDict
    
    def getPostContent(self, postID):
        # send a post ID to get content from
        response = self.post_service.GetPostContent(post_pb2.GetPostContentRequest(
            postID=postID
        ))

        # convert response into list of responses
        response_list = list(response)

        if len(response_list) == 0:
            return None

        # first response holds only type information - the rest are contents
        type = response_list[0].type
        content_list = response_list[1:]

        # type is an enum and is represent as a number
        # which is why i use this weird boolean
        if type == post_pb2.PostMeta(type="IMAGE").type:
            # if image, return first response's content as content
            return content_list[0].imageurl
        elif type == post_pb2.PostMeta(type="VIDEO").type:
            # if video, convert all frames from content into a list of frames
            return [content_list[x].videoframe for x in range(len(content_list))]
        else:
            return None
        
    def ratePost(self, postID, rating):
        # send postID to rate, plus rating of UPVOTE or DOWNVOTE
        response = self.post_service.RatePost(post_pb2.RatePostRequest(
            postID=postID,
            rating=rating
        ))

        if response == post_pb2.RatePostResponse():
            return None

        # just return score
        return response.meta.score

    def close(self):
        self.channel.close()

    def createComment(self, userID, content, state):

        if (userID == None or content == None):
            return None

        # send text content, the user poster, an initial state
        response = self.comment_service.CreateComment(comment_pb2.NewCommentRequest(
            author=user_pb2.User(
                UID = userID
            ),
            state = state,
            content=content
        ))
    
        # convert post response to python dictionary
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
        # send commentID to rate, plus rating of UPVOTE or DOWNVOTE
        response = self.comment_service.RateComment(comment_pb2.RateCommentRequest(
            commentID=commentID,
            rating=rating
        ))

        if(response == comment_pb2.RateCommentResponse()):
            return None

        return response.comment.score
    
    def getComment(self, commentID):
        # send a comment ID to get
        response = self.comment_service.GetComment(comment_pb2.GetCommentRequest(
            commentID=commentID
        ))

        if(response == comment_pb2.GetCommentResponse()):
            return None
    
        # convert response to python dictionary
        responseToDict = {
            "author":response.comment.author.UID,
            "score":response.comment.score,
            "state":response.comment.state,
            "published":response.comment.published,
            "content":response.comment.content,
            "ID":response.comment.ID,
        }

        return responseToDict
    
    """
    get N most upvoted comments from under a comment,
    and N most upvoted replies from under those comments
    """
    def getNCommentsFromComment(self, commentID, numComments):
        # send comment ID to retrieve comments from, and max number of comments to retrieve
        responses = self.comment_service.GetNComments(comment_pb2.GetNCommentsRequest(
            commentID=commentID,
            num_comments=numComments
        ))

        # python list to return
        toReturn = []
        # convert stream to list
        responses = list(responses)

        # go through each response - IN ORDER
        for response in responses:
            comment_object = {}

            # if comment is a comment (not a subcomment)
            if response.comment != comment_pb2.Comment():
                # parse comment data
                comment_object["author"] = response.comment.author.UID
                comment_object["score"] = response.comment.score
                comment_object["state"] = response.comment.state
                comment_object["published"] = response.comment.published
                comment_object["content"] = response.comment.content
                comment_object["ID"] = response.comment.ID
                comment_object["comment"] = []

                # append to list
                toReturn.append(comment_object)

            # if comment is a subcomment
            if response.subcomment != comment_pb2.Comment():
                # parse subcomment data
                comment_object["author"] = response.subcomment.author.UID
                comment_object["score"] = response.subcomment.score
                comment_object["state"] = response.subcomment.state
                comment_object["published"] = response.subcomment.published
                comment_object["content"] = response.subcomment.content
                comment_object["ID"] = response.subcomment.ID
                comment_object["comment"] = []

                # append subcomment UNDERNEATH most recently appended comment
                toReturn[-1]["comment"].append(comment_object)

        return toReturn
    
    """
    get N most upvoted comments from under a post
    """
    def getNCommentsFromPost(self, postID, numComments):
        # send post ID to retrieve comments from, and max number of comments to retrieve
        responses = self.post_service.GetNComments(post_pb2.GetNCommentsRequest(
            postID=postID,
            num_comments=numComments
        ))

        toReturn = []

        for response in list(responses):
            comment_object = {}
            
            # parse comment data
            comment_object["author"] = response.comment.author.UID
            comment_object["score"] = response.comment.score
            comment_object["state"] = response.comment.state
            comment_object["published"] = response.comment.published
            comment_object["content"] = response.comment.content
            comment_object["ID"] = response.comment.ID
            comment_object["has_replies"] = response.has_replies

            # append to list
            toReturn.append(comment_object)

        return toReturn