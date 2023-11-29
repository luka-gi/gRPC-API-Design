from concurrent import futures
import logging
import argparse

import grpc
import post_service

class ServerConfig():
    def __init__(self):
        self.port = "50051"

def parse_args(server_config: ServerConfig):
    parser = argparse.ArgumentParser(description="gRPC server")

    parser.add_argument('-p, --port', dest='port', type=str,
                        help="port to run server on",
                        default=server_config.port)

    args = parser.parse_args()

    server_config.port = args.port

# partial implementation from the official gRPC tutorial
def serve(server_config: ServerConfig):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    post_service.addPostService(server)

    server.add_insecure_port("[::]:" + server_config.port)
    server.start()
    print("Server started, listening on " + server_config.port)

    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    server_config = ServerConfig()
    parse_args(server_config)
    serve(server_config)
