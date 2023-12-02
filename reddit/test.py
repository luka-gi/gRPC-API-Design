from unittest.mock import Mock
import unittest
import sys

# import server_API
sys.path.append('server')
from server.server_API import server_gRPC_API
from server.reddit_server import ServerConfig
from server.database.DataBase_API import DataBase
sys.path.append('client')
from client.reddit_client import ClientConfig
from client.client_API import client_gRPC_API

def get_most_upvoted_reply(client, postID_to_get, max_comments_to_get, max_replies_to_get):

    # get first post 
    postmeta = client.getPostMeta(postID_to_get)
    post = client.getPostContent(postID_to_get)

    if not post or not postmeta:
        return None

    # get most upvoted comments
    comments = client.getNCommentsFromPost(postID_to_get, max_comments_to_get)
    
    if not comments:
        return None

    # get most upvoted replies and subreplies for most upvoted comments
    most_upvoted_comment = sorted(comments, key=lambda dict: -dict["score"])
    most_upvoted_commentID = most_upvoted_comment[0]["ID"]
    replies = client.getNCommentsFromComment(most_upvoted_commentID, max_replies_to_get)

    if not replies:
        return None

    # get most upvoted reply under most upvoted comment
    most_upvoted_reply = sorted(replies, key=lambda dict: -dict["score"])
    most_upvoted_reply = most_upvoted_reply[0]
        
    return most_upvoted_reply  

class TestSuiteGetMostUpvotedReply(unittest.TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.post = {
            "meta":{
                "ID":2023,
            },
            "content": "www.reddit.com",
        }
        self.post_comments = [
            {
                "ID":3,
                "score":10,
            },
        ]

    """
    positive test: a happy path combination where the most upvoted reply is returned
    """
    def test_suite_get_most_upvoted_reply_combo_1(self):
        expected = {
                "ID":35,
                "score":22,
                "comment":[
                    {
                        "ID":36,
                        "score":17,
                    },
                    {
                        "ID":37,
                        "score":22,
                    }
                ],
            }

        most_upvoted_subcomments = [
            {
                "ID":24,
                "score":-10,
                "comment":[
                    {
                        "ID":30,
                        "score":14,
                    },
                    {
                        "ID":37,
                        "score":19,
                    }
                ],
            },
            {
                "ID":17,
                "score":19,
                "comment":[
                    {
                        "ID":18,
                        "score":14,
                    },
                    {
                        "ID":38,
                        "score":19,
                    }
                ],
            },
            expected
        ]

        client = Mock()
        client.getPostMeta.return_value = self.post["meta"]
        client.getPostContent.return_value = self.post["content"]
        client.getNCommentsFromPost.return_value = self.post_comments
        client.getNCommentsFromComment.return_value = most_upvoted_subcomments

        actual = get_most_upvoted_reply(client, 0, 2, 2)

        self.assertEqual(expected, actual)

    """
    positive test: another happy path combination where the most upvoted reply
    is returned (different score and section in the array)
    """
    def test_suite_get_most_upvoted_reply_combo_2(self):
        expected = {
                "ID":40,
                "score":99,
                "comment":[
                    {
                        "ID":36,
                        "score":17,
                    },
                    {
                        "ID":37,
                        "score":22,
                    }
                ],
            }

        most_upvoted_subcomments = [
            {
                "ID":24,
                "score":-10,
                "comment":[
                    {
                        "ID":30,
                        "score":14,
                    },
                    {
                        "ID":37,
                        "score":19,
                    }
                ],
            },
            expected,
            {
                "ID":17,
                "score":19,
                "comment":[
                    {
                        "ID":18,
                        "score":14,
                    },
                    {
                        "ID":38,
                        "score":19,
                    }
                ],
            },
            {
                "ID":35,
                "score":22,
                "comment":[
                    {
                        "ID":36,
                        "score":17,
                    },
                    {
                        "ID":37,
                        "score":22,
                    }
                ],
            },
        ]

        client = Mock()
        client.getPostMeta.return_value = self.post["meta"]
        client.getPostContent.return_value = self.post["content"]
        client.getNCommentsFromPost.return_value = self.post_comments
        client.getNCommentsFromComment.return_value = most_upvoted_subcomments

        actual = get_most_upvoted_reply(client, 0, 2, 2)

        self.assertEqual(expected, actual)

    """
    if post metadata does not exist, function should gracefully return null
    """
    def test_suite_get_most_upvoted_reply_no_post_meta(self):
        expected = None

        most_upvoted_subcomments = [
            {
                "ID":24,
                "score":-10,
                "comment":[
                    {
                        "ID":30,
                        "score":14,
                    },
                    {
                        "ID":37,
                        "score":19,
                    }
                ],
            },
            {
                "ID":17,
                "score":19,
                "comment":[
                    {
                        "ID":18,
                        "score":14,
                    },
                    {
                        "ID":38,
                        "score":19,
                    }
                ],
            },
            {
                "ID":35,
                "score":22,
                "comment":[
                    {
                        "ID":36,
                        "score":17,
                    },
                    {
                        "ID":37,
                        "score":22,
                    }
                ],
            },
        ]

        client = Mock()
        client.getPostMeta.return_value = None
        client.getPostContent.return_value = self.post["content"]
        client.getNCommentsFromPost.return_value = self.post_comments
        client.getNCommentsFromComment.return_value = most_upvoted_subcomments

        actual = get_most_upvoted_reply(client, 0, 2, 2)

        self.assertEqual(expected, actual)

    """
    if post content does not exist, function should gracefully return null
    """
    def test_suite_get_most_upvoted_reply_no_post_content(self):
        expected = None

        most_upvoted_subcomments = [
            {
                "ID":24,
                "score":-10,
                "comment":[
                    {
                        "ID":30,
                        "score":14,
                    },
                    {
                        "ID":37,
                        "score":19,
                    }
                ],
            },
            {
                "ID":17,
                "score":19,
                "comment":[
                    {
                        "ID":18,
                        "score":14,
                    },
                    {
                        "ID":38,
                        "score":19,
                    }
                ],
            },
            {
                "ID":35,
                "score":22,
                "comment":[
                    {
                        "ID":36,
                        "score":17,
                    },
                    {
                        "ID":37,
                        "score":22,
                    }
                ],
            },
        ]

        client = Mock()
        client.getPostMeta.return_value = self.post["meta"]
        client.getPostContent.return_value = None
        client.getNCommentsFromPost.return_value = self.post_comments
        client.getNCommentsFromComment.return_value = most_upvoted_subcomments

        actual = get_most_upvoted_reply(client, 0, 2, 2)

        self.assertEqual(expected, actual)

    """
    if comments do not exist, function should gracefully return null
    """
    def test_suite_get_most_upvoted_reply_no_comments(self):
        expected = None

        most_upvoted_subcomments = [
            {
                "ID":24,
                "score":-10,
                "comment":[
                    {
                        "ID":30,
                        "score":14,
                    },
                    {
                        "ID":37,
                        "score":19,
                    }
                ],
            },
            {
                "ID":17,
                "score":19,
                "comment":[
                    {
                        "ID":18,
                        "score":14,
                    },
                    {
                        "ID":38,
                        "score":19,
                    }
                ],
            },
            {
                "ID":35,
                "score":22,
                "comment":[
                    {
                        "ID":36,
                        "score":17,
                    },
                    {
                        "ID":37,
                        "score":22,
                    }
                ],
            },
        ]

        client = Mock()
        client.getPostMeta.return_value = self.post["meta"]
        client.getPostContent.return_value = self.post["content"]
        client.getNCommentsFromPost.return_value = None
        client.getNCommentsFromComment.return_value = most_upvoted_subcomments

        actual = get_most_upvoted_reply(client, 0, 2, 2)

        self.assertEqual(expected, actual)

    """
    if comment does have replies, function should gracefully return null
    """
    def test_suite_get_most_upvoted_reply_no_replies(self):
        expected = None

        most_upvoted_subcomments = None

        client = Mock()
        client.getPostMeta.return_value = self.post["meta"]
        client.getPostContent.return_value = self.post["content"]
        client.getNCommentsFromPost.return_value = self.post_comments
        client.getNCommentsFromComment.return_value = most_upvoted_subcomments

        actual = get_most_upvoted_reply(client, 0, 2, 2)

        self.assertEqual(expected, actual)

    def test_suite_actual_server(self):
        # According to the in-memory database, this is the expected output:
        # See the database, in the structure 'Comments'
        # The comment under post with an ID of 0 has a high score comment of 0 with score 10
        # Under that comment, there is a comment with ID 1 with a score of 9 as the highest rating
        expected = {
            'author': 'testuser',
            'score': 9, 'state': 0, 
            'published': '11/30/23', 
            'content': 'example comments', 
            'ID': 1, 'comment': 
            [
                {
                    'author': 'testuser', 
                    'score': 39, 
                    'state': 0, 
                    'published': '11/30/23', 
                    'content': 'example comments', 
                    'ID': 2, 
                    'comment': []
                },
                {
                    'author': 'testuser', 
                    'score': -7, 
                    'state': 0, 
                    'published': '11/30/23', 
                    'content': 'example comments', 
                    'ID': 8, 
                    'comment': []
                }
            ]
        }

        server_config = ServerConfig()
        client_config = ClientConfig()
        database = DataBase()

        # start server
        server = server_gRPC_API(server_config, database)
        server.start()

        # start client
        client = client_gRPC_API(client_config)
        client.open()

        # run function under test
        actual = get_most_upvoted_reply(client,0,2,2)

        # end client and server
        client.close()

        server.stop()

        #compare responses
        self.assertDictEqual(expected, actual)

    def test_suite_actual_server_false(self):
        expected = None

        server_config = ServerConfig()
        client_config = ClientConfig()
        database = DataBase()

        # start server
        server = server_gRPC_API(server_config, database)
        server.start()

        # start client
        client = client_gRPC_API(client_config)
        client.open()

        # run function under test
        actual = get_most_upvoted_reply(client,99,2,2)

        # end client and server
        client.close()

        server.stop()

        #compare responses, should be none
        self.assertEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()
