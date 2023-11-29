from __future__ import print_function

import logging

import grpc
import post_pb2
import post_pb2_grpc

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
def run(client_config: ClientConfig):
    server_location = client_config.host + ":" + client_config.port
    with grpc.insecure_channel(server_location) as channel:
        print("Creating post...")
        stub = post_pb2_grpc.PostServiceStub(channel)

        response = stub.PostImage(post_pb2.NewImagePostRequest(
            meta=post_pb2.NewPostMeta(
                title="fakeTitle",
                text="fakeText",
                state="NORMAL",
            ),
            image=post_pb2.Image(url="http://")
        ))

        print("Post 1 received: ")
        print(response)

        response = stub.PostVideo(post_pb2.NewVideoPostRequest(
            meta=post_pb2.NewPostMeta(
                title="fakeTitle",
                text="fakeText",
                state="NORMAL",
            ),
            video=post_pb2.Video(frames=["frame45","frame46","frame47"])
        ))

        print("Post 2 received: ")
        print(response)

if __name__ == "__main__":
    logging.basicConfig()
    client_config = ClientConfig()
    run(client_config)
