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
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        post_pb2_grpc.add_PostServiceServicer_to_server(post_service.Poster(self.DBConn), self.server)
        comment_pb2_grpc.add_CommentServiceServicer_to_server(comment_service.Commenter(self.DBConn), self.server)

        self.server.add_insecure_port("[::]:" + self.port)

        self.server.start()

    def stop(self):
        self.server.stop(None)

    def listen_and_serve(self):
        try:
            self.server.wait_for_termination()
        except KeyboardInterrupt:
            print("\nterminating server")