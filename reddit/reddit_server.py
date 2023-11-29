from concurrent import futures
import logging

import grpc
import reddit_pb2
import reddit_pb2_grpc

class Poster(reddit_pb2_grpc.PostServiceServicer):
    def CreatePost(self, request, context):
        return reddit_pb2.Post(title="Hello, %s!" % request.title)

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
