"""
creates and implements the gRPC server
"""
from concurrent import futures

import sys
import grpc

sys.path.append("protos")
from protos import post_pb2_grpc
import post_service
from protos import comment_pb2_grpc
import comment_service

class server_gRPC_API:

    def __init__(self,client_config, database):
        self.port = client_config.port
        self.DB = database
        self.DBConn = self.DB.connect()
        self.server = None

    def start(self):
        # start the server with multiple threads
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        # add the implemented post and comment services to the gRPC server
        post_pb2_grpc.add_PostServiceServicer_to_server(post_service.Poster(self.DBConn), self.server)
        comment_pb2_grpc.add_CommentServiceServicer_to_server(comment_service.Commenter(self.DBConn), self.server)

        # define the port to start on
        self.server.add_insecure_port("[::]:" + self.port)

        # start the gRPC server
        self.server.start()

    def stop(self):
        # stop server with no grace period
        self.server.stop(None)

    def listen_and_serve(self):
        # poll until keyboard interrupt
        try:
            self.server.wait_for_termination()
        except KeyboardInterrupt:
            print("\nterminating server")