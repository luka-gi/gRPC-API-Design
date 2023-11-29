from concurrent import futures

import grpc
import post_pb2_grpc
import post_service

from database.DataBase_API import DataBase

class server_gRPC_API:

    def __init__(self,client_config):
        self.port = client_config.port
        self.DB = DataBase()
        self.DBConn = self.DB.connect()
        self.server = None

    def start(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        post_pb2_grpc.add_PostServiceServicer_to_server(post_service.Poster(self.DBConn), self.server)

        self.server.add_insecure_port("[::]:" + self.port)

        self.server.start()

    def listen_and_serve(self):
        self.server.wait_for_termination()