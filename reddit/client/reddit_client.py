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

def test_posting(client):

    print("\n\n")
    print("Testing post image")
    response = client.postImage("fakeTitle","fakeText","NORMAL","http://")

    print("Post 1 received: ")
    print(response)

    print("\n\n")
    print("Testing post video\n")
    response = client.postVideo("fakeVideoTitle","fakeVideoDesc","NORMAL",["frame45","frame46","frame47"])

    print("Post 2 received: ")
    print(response)

    print("\n\n")
    print("get post content of an image\n")
    response = client.getPostContent(0)

    print("Post 3 received: ")
    print(response)

    print("\n\n")
    print("get post content of a video\n")
    response = client.getPostContent(1)

    print("Post 4 received: ")
    print(response)

    print("\n\n")
    print("test upvote\n")
    response = client.ratePost(1, "UPVOTE")

    print("Post 5 received: ")
    print(response)

    print("\n\n")
    print("test downvote\n")
    response = client.ratePost(0, "DOWNVOTE")

    print("Post 6 received: ")
    print(response)

    print("\n\n")
    print("test get N comments from the post\n")
    response = client.getNCommentsFromPost(0, 2)

    print("Post 7 recieved")
    print(response)

def test_commenting(client):

    print("\n\n")
    print("test creating a comment\n")
    response = client.createComment("commenterUser", "test comment!!!", "NORMAL")

    print("Comment 1 recieved")
    print(response)

    print("\n\n")
    print("test rating a comment\n")
    response = client.rateComment(0, "UPVOTE")

    print("Comment 2 recieved")
    print(response)

    print("\n\n")
    print("test rating a comment\n")
    response = client.rateComment(10, "DOWNVOTE")

    print("Comment 3 recieved")
    print(response)

    print("\n\n")
    print("test getting N comments from a comment\n")
    response = client.getNCommentsFromComment(0, 2)

    print("Comment 4 recieved")
    print(response)

# partial implementation from the official gRPC tutorial
def start_client(client_config: ClientConfig):

    parse_args(client_config)

    client = client_API.client_gRPC_API(client_config)
  
    client.open()

    test_posting(client)

    test_commenting(client)

    client.close()

if __name__ == "__main__":
    logging.basicConfig()    
    start_client(ClientConfig())
