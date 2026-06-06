from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import PostSerializer, CommentSerializer
from . models import Post, Comment

class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    permission_classes = [AllowAny]
    serializer_class = PostSerializer

    def post(self, request, *args, **kwargs):
        print("data posted")
        return super().post(request, *args, **kwargs)
    

class PostUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [AllowAny]
    serializer_class = PostSerializer

    def get_object(self):
        return Post.objects.get(id=self.kwargs['pk'])

    def perform_update(self, serializer):
        return super().perform_update(serializer)
    
    def perform_destroy(self, instance):
        return super().perform_destroy(instance)
    
class HomeAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    permission_classes = [AllowAny]
    serializer_class = PostSerializer

class AddCommentAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CommentSerializer

    def get_object(self):
        return Post.objects.get(id=self.kwargs['id'])
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.post = self.get_object()
            serializer.save()
        