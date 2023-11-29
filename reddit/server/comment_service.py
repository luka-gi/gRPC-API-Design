import comment_pb2
import comment_pb2_grpc

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
            self.author,
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

        print(self.DBConn.getComments())

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
