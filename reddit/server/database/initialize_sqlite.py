import sqlite3
import json
from DataBase import database_in_mem

DB = database_in_mem()
conn = sqlite3.connect("./reddit.db")
cur = conn.cursor()

########################################
# create tables
cur.execute('''CREATE TABLE IF NOT EXISTS
users
(
    UID TEXT
)
''')

cur.execute('''CREATE TABLE IF NOT EXISTS
subreddits
(
    name TEXT,
    state TEXT,
    tags TEXT
)
''')

cur.execute('''CREATE TABLE IF NOT EXISTS
posts
(
    title TEXT,
    text TEXT,
    score INTEGER,
    state TEXT,
    published TEXT,
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    content TEXT,
    comment TEXT,
    subreddit TEXT,
    tags TEXT
)
''')

cur.execute('''CREATE TABLE IF NOT EXISTS
comments
(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    score INTEGER,
    author TEXT,
    state TEXT,
    published TEXT,
    content TEXT,
    comment TEXT
)
''')

########################################
# populate the databases
cur.executemany('''INSERT INTO
users
(
    UID
)
VALUES
(
    :UID
)
''',DB.Users)

# convert subreddits tag field to json object
subreddits = DB.SubReddits

for subreddit in subreddits:
    subreddit["tags"] = json.dumps(subreddit["tags"])

cur.executemany('''INSERT INTO
subreddits
(
    name,
    state,
    tags
)
VALUES
(
    :name,
    :state,
    :tags
)
''',subreddits)

# convert post fields to json object
posts = DB.Posts

for post in posts:
    post["content"] = json.dumps(post["content"])
    post["comment"] = json.dumps(post["comment"])
    post["subreddit"] = json.dumps(post["subreddit"])
    post["tags"] = json.dumps(post["tags"])

cur.executemany('''INSERT INTO
posts
(
    title,
    text,
    score,
    state,
    published,
    ID,
    type,
    content,
    comment,
    subreddit,
    tags
)
VALUES
(
    :title,
    :text,
    :score,
    :state,
    :published,
    :ID,
    :type,
    :content,
    :comment,
    :subreddit,
    :tags
)
''',posts)

# convert comments fields to json object
comments = DB.Comments

for comment in comments:
    comment["comment"] = json.dumps(comment["comment"])

cur.executemany('''INSERT INTO
comments
(
    ID,
    score,
    author,
    state,
    published,
    content,
    comment
)
VALUES
(
    :ID,
    :score,
    :author,
    :state,
    :published,
    :content,
    :comment
)
''',comments)

########################################
# test getting db items, print to console
cur.execute('SELECT * FROM users')
print(cur.fetchmany(2))
cur.execute('SELECT * FROM subreddits')
print()
for subreddit in cur.fetchmany(2):
    print(subreddit)
    print(type(subreddit))
    print(subreddit[2])
    print(type(json.loads(subreddit[2])))
    print(json.loads(subreddit[2]))
print()
cur.execute('SELECT * FROM posts')
for post in cur.fetchmany(2):
    print(post)
    print(json.loads(post[7]))
    print(json.loads(post[8]))
    print(json.loads(post[9]))
    print(json.loads(post[10]))
cur.execute('SELECT * FROM comments')
print()
for comment in cur.fetchmany(2):
    print(comment)
    print(json.loads(comment[6]))


conn.commit()
# close connections
cur.close()
conn.close()