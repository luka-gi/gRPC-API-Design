import grpc
import post_pb2_grpc
import post_pb2

class client_gRPC_API:

    def __init__(self,client_config):
        self.port = client_config.port
        self.host = client_config.host
        self.channel = None
        self.post_service = None

    def open(self):
        server_location = self.host + ":" + self.port

        self.channel = grpc.insecure_channel(server_location)

        self.post_service = post_pb2_grpc.PostServiceStub(self.channel)

    def postImage(self, title, text, state, image_url):
        return self.post_service.PostImage(post_pb2.NewImagePostRequest(
            meta=post_pb2.NewPostMeta(
                title=title,
                text=text,
                state=state,
            ),
            image=post_pb2.Image(url=image_url)
        ))
    
    def postVideo(self, title, text, state, video_frames):
        return self.post_service.PostVideo(post_pb2.NewVideoPostRequest(
            meta=post_pb2.NewPostMeta(
                title=title,
                text=text,
                state=state,
            ),
            video=post_pb2.Video(frames=video_frames)
        ))
    
    def getPostContent(self, postID):
        response = self.post_service.GetPostContent(post_pb2.GetPostContentRequest(
            postID=postID
        ))

        return list(response)

    def close(self):
        self.channel.close()