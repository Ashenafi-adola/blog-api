from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import PostSerializer, CommentSerializer
from . models import Post, Comment

class PostCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    permission_classes = [AllowAny]
    serializer_class = PostSerializer
    