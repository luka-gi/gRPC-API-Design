class database_in_mem:
    Users = [
        {
            "UID": "testuser",
        },
        {
            "UID": "testuser2"
        }
    ]

    CommentID = 1

    Comments = [
        {
            "ID": 0,
            "score": 3,
            "author": "testuser",
            "state": "NORMAL",
            "published": "11/30/23",
            "content": "example comments"
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
            "content": "http://kasjfdklsajfdlkj"
        },
        {
            "title": "testTitle2",
            "text": "testText2",
            "score": -3,
            "state": "NORMAL",
            "published": "11/28/2023",
            "ID": 1,
            "type": "VIDEO",
            "content":["frame1","frame2","frame3"]
        },
    ]