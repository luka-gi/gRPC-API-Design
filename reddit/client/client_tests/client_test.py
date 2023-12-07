"""
simply a list of all available services and their different options
testing if their happy paths work (i.e., do they send readable data)
"""

def test_posting(client):

    print("\n\n")
    print("Testing post image")
    response = client.postImage("fakeTitle","fakeText","NORMAL","http://","subreddit1",["tag1","tag2"])

    print("Post 1 received: ")
    print(response)

    print("\n\n")
    print("Testing post video\n")
    response = client.postVideo("fakeVideoTitle","fakeVideoDesc","NORMAL",["frame45","frame46","frame47"],"subreddit2",["tag5","tag6"])

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

    # print("\n\n")
    # print("test get N comments from the post\n")
    # response = client.getNCommentsFromPost(0, 2)

    # print("Post 7 recieved")
    # print(response)

    # print("\n\n")
    # print("test get a post from the ID\n")
    # response = client.getPostMeta(0)

    # print("Post 8 recieved")
    # print(response)

def test_commenting(client):

    print("\n\n")
    print("test creating a comment\n")
    response = client.createComment("commenterUser", "test comment!!!", "NORMAL")

    print("Comment 1 recieved")
    print(response)

    # print("\n\n")
    # print("test rating a comment\n")
    # response = client.rateComment(0, "UPVOTE")

    # print("Comment 2 recieved")
    # print(response)

    # print("\n\n")
    # print("test rating a comment\n")
    # response = client.rateComment(10, "DOWNVOTE")

    # print("Comment 3 recieved")
    # print(response)

    # print("\n\n")
    # print("test getting N comments from a comment\n")
    # response = client.getNCommentsFromComment(0, 2)

    # print("Comment 4 recieved")
    # print(response)

    # print("\n\n")
    # print("test get a comments from the ID\n")
    # response = client.getComment(0)

    # print("Comment 5 recieved")
    # print(response)

def test_commenting_invalid(client):
    print("\n\n")
    print("test creating invalid comment\n")
    response = client.createComment(None, None, "NORMAL")

    print("Comment 1 recieved")
    print(response)

    print("\n\n")
    print("test rating invalid comment\n")
    response = client.rateComment(99, "UPVOTE")

    print("Comment 2 recieved")
    print(response)

    print("\n\n")
    print("test rating invalid comment\n")
    response = client.rateComment(99, "DOWNVOTE")

    print("Comment 3 recieved")
    print(response)

    print("\n\n")
    print("test getting N comments from invalid comment\n")
    response = client.getNCommentsFromComment(99, 2)

    print("Comment 4 recieved")
    print(response)

    print("\n\n")
    print("test get a comments from invalid ID\n")
    response = client.getComment(99)

    print("Comment 5 recieved")
    print(response)

def test_posting_invalid(client):
    print("\n\n")
    print("Testing post image")
    response = client.postImage(None,None,"NORMAL",None,None,None)

    print("Post 1 received: ")
    print(response)

    print("\n\n")
    print("Testing post video\n")
    response = client.postVideo(None,None,"NORMAL",None,None,None)

    print("Post 2 received: ")
    print(response)

    print("\n\n")
    print("get post content of invalid image\n")
    response = client.getPostContent(99)

    print("Post 3 received: ")
    print(response)

    print("\n\n")
    print("get post content of invalid video\n")
    response = client.getPostContent(99)

    print("Post 4 received: ")
    print(response)

    print("\n\n")
    print("test invalid upvote\n")
    response = client.ratePost(99, "UPVOTE")

    print("Post 5 received: ")
    print(response)

    print("\n\n")
    print("test invalid downvote\n")
    response = client.ratePost(99, "DOWNVOTE")

    print("Post 6 received: ")
    print(response)

    print("\n\n")
    print("test get N comments from invalid post\n")
    response = client.getNCommentsFromPost(99, 2)

    print("Post 7 recieved")
    print(response)

    print("\n\n")
    print("test get a post from invalid ID\n")
    response = client.getPostMeta(99)

    print("Post 8 recieved")
    print(response)

def test_bonus(client):
    print("\n\n")
    print("test bonus service\n")
    response = client.monitorPostScore(0, [0,7,10])

    print("Monitor recieved")
    print(response)

class client_test:
    def run(client):
        print("starting basic test\n")
        test_posting(client)
        test_commenting(client)
        
        # test_commenting_invalid(client)
        # test_posting_invalid(client)
        
        # test_bonus(client)