import comment_pb2
import comment_pb2_grpc
import user_pb2

from datetime import datetime

class Comment:
    def __init__(self,DBConn,request):
        self.score = 0
        self.published=datetime.today().strftime('%m/%d/%Y')
        self.content = request.content
        self.state = request.state
        self.ID = DBConn.getNewCommentID()
        self.author = request.author

    def addNewCommentToDatabase(self, DBConn):
        DBConn.addNewComment(
            self.score,
            self.published,
            self.state,
            self.content,
            self.ID,
            self.author.UID,
        )

class Commenter(comment_pb2_grpc.CommentServiceServicer):

    def __init__(self, DBConn):
        super().__init__()
        self.DBConn = DBConn

    def CreateComment(self, request, context):
        print(request)

        # parse request
        NewComment = Comment(self.DBConn,request)

        # add comment to DB
        NewComment.addNewCommentToDatabase(self.DBConn)

        return comment_pb2.NewCommentResponse(
            comment=comment_pb2.Comment(
                score = NewComment.score,
                published = NewComment.published,
                content = NewComment.content,
                state = NewComment.state,
                ID = NewComment.ID,
                author = NewComment.author,
            )
        )
    
    def RateComment(self, request, contex):
        if request.commentID == None:
            return None
        
        comment = self.DBConn.rateComment(request.commentID, request.rating)

        if not comment:
            return None
        
        RateCommentResponse = comment_pb2.RateCommentResponse(
            comment=comment_pb2.Comment(
                score = comment["score"],
                published = comment["published"],
                content = comment["content"],
                state = comment["state"],
                ID = comment["ID"],
                author = user_pb2.User(
                    UID=comment["author"],
                )
            )
        )

        return RateCommentResponse
    
    def GetNComments(self, request, context):
        if request.commentID == None:
            return None
        
        comment = self.DBConn.getCommentByID(request.commentID)

        if not comment:
            return None
        
        comments = []

        sorted_comments = sorted(comment["comment"], key=lambda dict: -dict["score"])

        for i,subcomment in enumerate(sorted_comments):
            if i < request.num_comments:
                sorted_subcomments = sorted(subcomment["comment"], key=lambda dict: -dict["score"])

                for j,subsubcomment in enumerate(sorted_subcomments):
                    if j < request.num_comments:
                        comments.append(comment_pb2.Comment(
                            score = subsubcomment["score"],
                            published = subsubcomment["published"],
                            content = subsubcomment["content"],
                            state = subsubcomment["state"],
                            ID = subsubcomment["ID"],
                            author = user_pb2.User(
                                UID=subsubcomment["author"],
                            )   
                        ))

                comments.append(comment_pb2.Comment(
                    score = subcomment["score"],
                    published = subcomment["published"],
                    content = subcomment["content"],
                    state = subcomment["state"],
                    ID = subcomment["ID"],
                    author = user_pb2.User(
                        UID=subcomment["author"],
                    )   
                ))
        
        return comment_pb2.GetNCommentsResponse(
            comment=comments
        )
