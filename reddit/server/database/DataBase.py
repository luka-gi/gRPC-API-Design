class database_in_mem:
    Users = [
        {
            "UID": "testuser",
        },
        {
            "UID": "testuser2"
        }
    ]

    CommentID = 12

    Comments = [
        {
            "ID": 0,
            "score": 1000,
            "author": "testuser",
            "state": "NORMAL",
            "published": "11/30/23",
            "content": "example comments",
            "comment": [
                {
                    "ID": 1,
                    "score": 99,
                    "author": "testuser",
                    "state": "NORMAL",
                    "published": "11/30/23",
                    "content": "example comments",
                    "comment":[
                        {
                            "ID": 2,
                            "score": 39,
                            "author": "testuser",
                            "state": "NORMAL",
                            "published": "11/30/23",
                            "content": "example comments",
                            "comment":[
                                {
                                    "ID": 3,
                                    "score": 3,
                                    "author": "testuser",
                                    "state": "NORMAL",
                                    "published": "11/30/23",
                                    "content": "example comments",
                                    "comment":[]
                                }
                            ]
                        },
                        {
                            "ID": 7,
                            "score": -19,
                            "author": "testuser",
                            "state": "NORMAL",
                            "published": "11/30/23",
                            "content": "example comments",
                            "comment":[]
                        },
                        {
                            "ID": 8,
                            "score": -7,
                            "author": "testuser",
                            "state": "NORMAL",
                            "published": "11/30/23",
                            "content": "example comments",
                            "comment":[]
                        }
                    ]
                },
                {
                    "ID": 4,
                    "score": -3,
                    "author": "testuser",
                    "state": "NORMAL",
                    "published": "11/30/23",
                    "content": "example comments",
                    "comment": []
                },
                {
                    "ID": 5,
                    "score": 4,
                    "author": "testuser",
                    "state": "NORMAL",
                    "published": "11/30/23",
                    "content": "example comments",
                    "comment": []
                },
            ]
        },
        {
            "ID": 9,
            "score": 3,
            "author": "testuser",
            "state": "NORMAL",
            "published": "11/30/23",
            "content": "example comments",
            "comment": []
        },
        {
            "ID": 10,
            "score": 3,
            "author": "testuser",
            "state": "NORMAL",
            "published": "11/30/23",
            "content": "example comments",
            "comment": []
        },
        {
            "ID": 11,
            "score": 3,
            "author": "testuser",
            "state": "NORMAL",
            "published": "11/30/23",
            "content": "example comments",
            "comment": []
        }
    ]

    SubReddits = [
        {
            "name": "subreddit1",
            "state": "PUBLIC",
            "tags": ["tag1","tag2","tag3"]
        },
        {
            "name": "subreddit2",
            "state": "PUBLIC",
            "tags": ["tag4","tag5","tag6"]
        },
    ]

    PostID = 2

    Posts = [
        {
            "title": "testTitle",
            "text": "testText",
            "score": 40,
            "state": "NORMAL",
            "published": "11/28/2023",
            "ID": 0,
            "type": "IMAGE",
            "content": "http://kasjfdklsajfdlkj",
            "comment": [Comments[0],Comments[1],Comments[2]],
            "subreddit": SubReddits[0],
            "tags": ["tag1","tag2","tag3"]
        },
        {
            "title": "testTitle2",
            "text": "testText2",
            "score": -3,
            "state": "NORMAL",
            "published": "11/28/2023",
            "ID": 1,
            "type": "VIDEO",
            "content":["frame1","frame2","frame3"],
            "comment": [Comments[3]],
            "subreddit": SubReddits[1],
            "tags": ["tag4","tag5","tag6"]
        },
    ]