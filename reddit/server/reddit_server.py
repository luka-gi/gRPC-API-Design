from concurrent import futures
import logging

import grpc
import reddit_pb2
import reddit_pb2_grpc

from DataBase import DB
from datetime import datetime

class Poster(reddit_pb2_grpc.PostServiceServicer):

    class NewPostMetaData():
        def __init__(self):
            self.score = 0
            self.published = datetime.today().strftime('%m/%d/%Y')
            self.ID = DB.PostID
            DB.PostID = DB.PostID + 1

    def requestValidated(self,request):
        if not (request.meta.title and request.meta.text and request.meta.state):
            return False

        return True

    def PostImage(self, request, context):
        if not self.requestValidated(request):
            return None

        if not request.image.url:
            return None

        meta = self.NewPostMetaData()
        meta.type = "IMAGE"

        DB.Posts.append({
            "title": request.meta.title,
            "text": request.meta.text,
            "score": meta.score,
            "state": request.meta.state,
            "published": meta.published,
            "ID": meta.ID,
            "type": meta.type,
            "content": request.image.url,
        })

        print(DB.Posts)

        return reddit_pb2.Post(
            title=request.meta.title,
            text=request.meta.text,
            score=meta.score,
            state=request.meta.state,
            published=meta.published,
            ID=meta.ID,
            type=meta.type,
            image=request.image,
        )

# partial implementation from the official gRPC tutorial
def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    reddit_pb2_grpc.add_PostServiceServicer_to_server(Poster(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
