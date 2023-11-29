from concurrent import futures
import logging

import grpc
import reddit_pb2
import reddit_pb2_grpc

from DataBase import DB
from datetime import datetime

class Poster(reddit_pb2_grpc.PostServiceServicer):

    def populatePostMetadata(self, request):
        newImage = reddit_pb2.Post(
            score=0,
            published=datetime.today().strftime('%m/%d/%Y'),
            ID=DB.PostID,
            title=request.meta.title,
            text=request.meta.text,
            state=request.meta.state,
        )

        DB.PostID = DB.PostID + 1

        return newImage

    def requestValidated(self,request):
        if not (request.meta.title and request.meta.text and request.meta.state):
            return False

        return True

    def PostImage(self, request, context):
        if not self.requestValidated(request):
            return None

        if not request.image.url:
            return None

        type = "IMAGE"

        newImage = self.populatePostMetadata(request)

        # populate image-specifics to post
        newImage.type = type
        newImage.image.CopyFrom(request.image)

        # add to DB
        # take enums from request
        DB.Posts.append({
            "title": newImage.title,
            "text": newImage.text,
            "score": newImage.score,
            "state": request.meta.state,
            "published": newImage.published,
            "ID": newImage.ID,
            "type": type,
            "content": newImage.image.url,
        })
        print(DB.Posts)

        return newImage

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
