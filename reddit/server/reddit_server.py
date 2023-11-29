from concurrent import futures
import logging

import grpc
import reddit_pb2
import reddit_pb2_grpc

from DataBase import DB
from datetime import datetime
from google.protobuf.json_format import MessageToJson
import json

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
            "title": request.meta.title,
            "text": request.meta.text,
            "score": newImage.score,
            "state": request.meta.state,
            "published": newImage.published,
            "ID": newImage.ID,
            "type": type,
            "content": request.image.url,
        })
        print(DB.Posts)

        return newImage

    def PostVideo(self, request, context):
        if not self.requestValidated(request):
            return None

        if not request.video.frames:
            return None

        type = "VIDEO"

        newVideo = self.populatePostMetadata(request)

        # populate image-specifics to post
        newVideo.type = type
        newVideo.video.CopyFrom(request.video)

        # add to DB
        # take enums from request
        DB.Posts.append({
            "title": request.meta.title,
            "text": request.meta.text,
            "score": newVideo.score,
            "state": request.meta.state,
            "published": newVideo.published,
            "ID": newVideo.ID,
            "type": type,
            "content": request.video.frames,
        })
        print(DB.Posts)

        return newVideo

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
