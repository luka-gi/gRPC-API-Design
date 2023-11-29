from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class User(_message.Message):
    __slots__ = ["UID"]
    UID_FIELD_NUMBER: _ClassVar[int]
    UID: str
    def __init__(self, UID: _Optional[str] = ...) -> None: ...

class Post(_message.Message):
    __slots__ = ["title", "text", "score", "state", "published", "ID"]
    class PostState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        NORMAL: _ClassVar[Post.PostState]
        LOCKED: _ClassVar[Post.PostState]
        HIDDEN: _ClassVar[Post.PostState]
    NORMAL: Post.PostState
    LOCKED: Post.PostState
    HIDDEN: Post.PostState
    TITLE_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    PUBLISHED_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    title: str
    text: str
    score: int
    state: Post.PostState
    published: str
    ID: str
    def __init__(self, title: _Optional[str] = ..., text: _Optional[str] = ..., score: _Optional[int] = ..., state: _Optional[_Union[Post.PostState, str]] = ..., published: _Optional[str] = ..., ID: _Optional[str] = ...) -> None: ...

class Comment(_message.Message):
    __slots__ = ["author", "score", "state", "published"]
    class CommentState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        NORMAL: _ClassVar[Comment.CommentState]
        HIDDEN: _ClassVar[Comment.CommentState]
    NORMAL: Comment.CommentState
    HIDDEN: Comment.CommentState
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    PUBLISHED_FIELD_NUMBER: _ClassVar[int]
    author: User
    score: str
    state: Comment.CommentState
    published: str
    def __init__(self, author: _Optional[_Union[User, _Mapping]] = ..., score: _Optional[str] = ..., state: _Optional[_Union[Comment.CommentState, str]] = ..., published: _Optional[str] = ...) -> None: ...

class NewPostRequest(_message.Message):
    __slots__ = ["title", "text", "state"]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    title: str
    text: str
    state: str
    def __init__(self, title: _Optional[str] = ..., text: _Optional[str] = ..., state: _Optional[str] = ...) -> None: ...
