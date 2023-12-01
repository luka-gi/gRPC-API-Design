import logging

import sys
sys.path.append("server")
sys.path.append("client")

from server import server_API
from server.database.DataBase_API import DataBase
from client import client_API
from server.reddit_server import ServerConfig
from client.reddit_client import ClientConfig
from client.client_tests.client_test import client_test

def test_assignment(client, postID_to_get, max_comments_to_get, max_replies_to_get):
    postID_to_get = 0
    max_comments_to_get = 2
    max_replies_to_get = 2

    # get first post 
    post = client.getPostContent(postID_to_get)

    print("\npost " + str(postID_to_get) + " content:\n")
    print(post)

    # get most upvoted comments
    comments = client.getNCommentsFromPost(postID_to_get, max_comments_to_get)

    print("\n" + str(max_comments_to_get) + " most upvoted comments:\n")
    print(comments)

    # get most upvoted replies and subreplies for most upvoted comments
    most_upvoted_comment = sorted(comments, key=lambda dict: -dict["score"])
    most_upvoted_commentID = most_upvoted_comment[0]["ID"]
    replies = client.getNCommentsFromComment(most_upvoted_commentID, max_replies_to_get)

    print("\n" + str(max_replies_to_get) + " most upvoted replies:")
    
    for reply in replies:
        print("\nreply")
        print(reply)
        for subreply in reply["comment"]:
            print("\nsubcomment:")
            print(subreply)

    # get most upvoted reply under most upvoted comment
    most_upvoted_reply = sorted(replies, key=lambda dict: -dict["score"])
    most_upvoted_reply = most_upvoted_reply[0]
    
    #return most upvoted reply, null otherwise
    if not most_upvoted_reply:
        return None
    
    return most_upvoted_reply
        

if __name__ == "__main__":
    logging.basicConfig()

    # mock database
    database = DataBase()
    server_config = ServerConfig()
    # start actual server as SUT
    server = server_API.server_gRPC_API(server_config,database)
    server.start()
    print("Server started, listening on " + server_config.port)

    # create mock client
    client = client_API.client_gRPC_API(ClientConfig())
    client.open()

    # run client tests
    most_upvoted_reply = test_assignment(client=client, 
                                         postID_to_get=0,
                                         max_comments_to_get=2,
                                         max_replies_to_get=2)
    
    # check response
    print("\nmost upvoted reply:\n")
    print(most_upvoted_reply)    

    server.stop()
