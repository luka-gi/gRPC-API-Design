from __future__ import print_function

import logging

import client_API

import argparse

from client_tests.client_test import client_test

class ClientConfig():
    def __init__(self):
        self.host = "localhost"
        self.port = "50051"
        self.test = False

def parse_args(client_config: ClientConfig):
    parser = argparse.ArgumentParser(description="gRPC server")

    parser.add_argument('-H, --host', dest='host', type=str,
                    help="hostname where server can be found",
                    default=client_config.host)
    parser.add_argument('-p, --port', dest='port', type=str,
                    help="port where server can be found",
                    default=client_config.port)
    parser.add_argument('-t, --test', dest='test', action='store_true',
                    help="basic tests I used during implementation, no actual validation implemented",
                    default=client_config.test)

    args = parser.parse_args()

    client_config.port = args.port
    client_config.host = args.host
    client_config.test = args.test

# partial implementation from the official gRPC tutorial
def start_client(client_config: ClientConfig):

    parse_args(client_config)

    client = client_API.client_gRPC_API(client_config)
  
    client.open()

    if client_config.test:
        client_test.run(client)

    # put client requests here

    client.close()

if __name__ == "__main__":
    logging.basicConfig()    
    start_client(ClientConfig())
