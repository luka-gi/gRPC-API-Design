from concurrent import futures
import logging

import grpc
import reddit_pb2
import reddit_pb2_grpc

from DataBase import DB
from datetime import datetime

class Poster(reddit_pb2_grpc.PostServiceServicer):
    def CreatePost(self, request, context):
        if not (request.title and request.text and request.state):
            return None
        
        score = 0
        published = datetime.today().strftime('%m/%d/%Y')
        ID = DB.PostID
        DB.PostID = DB.PostID + 1

        DB.Posts.append({
            "title": request.title,
            "text": request.text,
            "score": score,
            "state": request.state,
            "published": published,
            "ID": ID,
        })

        print(DB.Posts)

        return reddit_pb2.Post(
            title=request.title,
            text=request.title,
            score=score,
            state=request.state,
            published=published,
            ID=ID
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
