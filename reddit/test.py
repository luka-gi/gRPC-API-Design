import logging

import sys
sys.path.append("server")
sys.path.append("client")

from server import server_API
from client import client_API
from server.reddit_server import ServerConfig
from client.reddit_client import ClientConfig
from client.client_tests.client_test import client_test

def test_retrieve_post(client):
    pass

def test_retrieve_most_upvoted_comment_from_post(client):
    pass

def test_expand_most_upvoted_comment(client):
    pass

def test_return_most_upvoted_reply(client):
    pass

if __name__ == "__main__":
    logging.basicConfig()

    # client = client_API.client_gRPC_API(ClientConfig())
    # client.open()
    # client_test.run(client)
    # client.close()

    # server_config = ServerConfig()
    # server = server_API.server_gRPC_API(server_config)
    # server.start()
    # print("Server started, listening on " + server_config.port)
    # server.listen_and_serve()

    # test_retrieve_post(None)
    # test_retrieve_most_upvoted_comment_from_post(None)
    # test_expand_most_upvoted_comment(None)
    # test_return_most_upvoted_reply(None)