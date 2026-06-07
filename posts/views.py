from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, DislikeSerializer
from . models import Post, Comment, Like,Dislike
from rest_framework.exceptions import PermissionDenied

class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        if serializer.is_valid():
            instance = serializer.save(user=self.request.user)
            Like.objects.create(post=instance)
            Dislike.objects.create(post=instance)
    

class PostUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_object(self):
        return Post.objects.get(id=self.kwargs['pk'])

    def perform_update(self, serializer):
        return super().perform_update(serializer)
    
    def perform_destroy(self, instance):
        if instance.user == self.request.user:
            return super().perform_destroy(instance)
        else:
            raise PermissionDenied("only the owner of the post can delete this post")
    
class HomeAPIView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-posted_at')
    permission_classes = [AllowAny]
    serializer_class = PostSerializer

class AddCommentAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs['pk']).order_by('-date')

    def get_object(self):
        return Post.objects.get(id=self.kwargs['pk'])
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(post=self.get_object())

class LikeAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Like.objects.all()
    
    def get_object(self):
        post = Post.objects.get(id=self.kwargs['pk'])
        instance, created = Like.objects.get_or_create(post=post)
        return instance

    def put(self, request, *args, **kwargs):
        print(request.data)
        return super().put(request, *args, **kwargs)
    def perform_update(self, serializer):
        serializer.save()