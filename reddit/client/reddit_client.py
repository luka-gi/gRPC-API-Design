from __future__ import print_function

import logging

import grpc
import reddit_pb2
import reddit_pb2_grpc

# partial implementation from the official gRPC tutorial
def run():
    print("Createing post...")
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = reddit_pb2_grpc.PostServiceStub(channel)

        response = stub.CreatePost(reddit_pb2.NewPostRequest(
            title="fakeTitle",
            text="fakeText",
            state="NORMAL",
        ))

        print("Post received: ")
        print(response)

if __name__ == "__main__":
    logging.basicConfig()
    run()
