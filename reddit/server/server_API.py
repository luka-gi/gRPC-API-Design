from concurrent import futures

import grpc
import post_pb2_grpc
import post_service

class server_gRPC_API:

    def __init__(self,client_config):
        self.port = client_config.port
        self.server = None

    def start(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        post_pb2_grpc.add_PostServiceServicer_to_server(post_service.Poster(), self.server)

        self.server.add_insecure_port("[::]:" + self.port)

        self.server.start()

    def listen_and_serve(self):
        self.server.wait_for_termination()