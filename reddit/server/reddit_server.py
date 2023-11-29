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

    def createImagePostResponse(self, request):
        type = "IMAGE"

        newImage = reddit_pb2.ImagePostResponse(
            meta=reddit_pb2.PostMeta(
                score=0,
                published=datetime.today().strftime('%m/%d/%Y'),
                ID=DB.PostID,
                title=request.meta.title,
                text=request.meta.text,
                type=type,
                state=request.meta.state,
            ),
            image=request.image,
        )

        DB.PostID = DB.PostID + 1

        return newImage

    def createVideoPostResponse(self, request):
        type = "VIDEO"

        newVideo = reddit_pb2.VideoPostResponse(
            meta=reddit_pb2.PostMeta(
                score=0,
                published=datetime.today().strftime('%m/%d/%Y'),
                ID=DB.PostID,
                title=request.meta.title,
                text=request.meta.text,
                type=type,
                state=request.meta.state,
            ),
            video=request.video,
        )

        DB.PostID = DB.PostID + 1

        return newVideo

    def requestValidated(self,request):
        if not (request.meta.title and request.meta.text and request.meta.state):
            return False

        return True

    def PostImage(self, request, context):
        if not self.requestValidated(request):
            return None

        if not request.image.url:
            return None

        newImage = self.createImagePostResponse(request)

        # add to DB
        # take enums from request
        DB.Posts.append({
            "score": newImage.meta.score,
            "published": newImage.meta.published,
            "ID": newImage.meta.ID,
            "title": request.meta.title,
            "text": request.meta.text,
            "state": request.meta.state,
            "type": "IMAGE",
            "content": request.image.url,
        })
        print(DB.Posts)

        return newImage

    def PostVideo(self, request, context):
        if not self.requestValidated(request):
            return None

        if not request.video.frames:
            return None

        newVideo = self.createVideoPostResponse(request)

        # add to DB
        # take enums from request
        DB.Posts.append({
            "score": newVideo.meta.score,
            "published": newVideo.meta.published,
            "ID": newVideo.meta.ID,
            "title": request.meta.title,
            "text": request.meta.text,
            "state": request.meta.state,
            "type": "VIDEO",
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
