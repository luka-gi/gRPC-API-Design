from unittest.mock import Mock
import unittest
import sys

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

if __name__ == "__main__":
    if len(sys.argv) > 1:
        TestSuiteGetMostUpvotedReply.print_flag = sys.argv.pop()

    unittest.main()
