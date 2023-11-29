from concurrent import futures
import logging

import grpc
from post_pb2_grpc import add_PostServiceServicer_to_server

import post_service

# partial implementation from the official gRPC tutorial
def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_PostServiceServicer_to_server(post_service.Poster(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
