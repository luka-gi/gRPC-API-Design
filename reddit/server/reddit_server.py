from concurrent import futures
import logging
import argparse

import server_API
from database.DataBase_API import DataBase

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
def serve(server_config: ServerConfig, database: DataBase):
    parse_args(server_config)

    server = server_API.server_gRPC_API(server_config, database)
  
    server.start()

    print("Server started, listening on " + server_config.port)

    server.listen_and_serve()


if __name__ == "__main__":
    logging.basicConfig()
    serve(ServerConfig(), DataBase())
