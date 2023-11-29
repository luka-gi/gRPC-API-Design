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

        response = stub.PostImage(reddit_pb2.NewImagePostRequest(
            meta=reddit_pb2.NewPostMeta(
                title="fakeTitle",
                text="fakeText",
                state="NORMAL",
            ),
            image=reddit_pb2.Image(url="http://")
        ))

        print("Post 1 received: ")
        print(response)

        response = stub.PostVideo(reddit_pb2.NewVideoPostRequest(
            meta=reddit_pb2.NewPostMeta(
                title="fakeTitle",
                text="fakeText",
                state="NORMAL",
            ),
            video=reddit_pb2.Video(frames=["frame45","frame46","frame47"])
        ))

        print("Post 2 received: ")
        print(response)

if __name__ == "__main__":
    logging.basicConfig()
    run()
