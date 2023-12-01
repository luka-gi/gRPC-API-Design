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
            "score": 10,
            "author": "testuser",
            "state": "NORMAL",
            "published": "11/30/23",
            "content": "example comments",
            "comment": [
                {
                    "ID": 1,
                    "score": 9,
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
            "comment": [Comments[0],Comments[1],Comments[2]]
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
            "comment": [Comments[3]]
        },
    ]