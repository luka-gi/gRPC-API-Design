from __future__ import print_function

import logging

import client_API

import argparse

class ClientConfig():
    def __init__(self):
        self.host = "localhost"
        self.port = "50051"

def parse_args(client_config: ClientConfig):
    parser = argparse.ArgumentParser(description="gRPC server")

    parser.add_argument('-H, --host', dest='host', type=str,
                    help="hostname where server can be found",
                    default=client_config.host)
    parser.add_argument('-p, --port', dest='port', type=str,
                        help="port where server can be found",
                        default=client_config.port)

    args = parser.parse_args()

    client_config.port = args.port
    client_config.host = args.host

# partial implementation from the official gRPC tutorial
def start_client(client_config: ClientConfig):

    parse_args(client_config)

    client = client_API.client_gRPC_API(client_config)
  
    client.open()

    print("Creating post...")

    response = client.postImage("fakeTitle","fakeText","NORMAL","http://")

    print("Post 1 received: ")
    print(response)

    response = client.postVideo("fakeVideoTitle","fakeVideoDesc","NORMAL",["frame45","frame46","frame47"])

    print("Post 2 received: ")
    print(response)

    response = client.getPostContent(0)

    print("Post 3 received: ")
    print(response)

    response = client.getPostContent(1)

    print("Post 4 received: ")
    print(response)

    client.close()

if __name__ == "__main__":
    logging.basicConfig()    
    start_client(ClientConfig())
