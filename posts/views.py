from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import PostSerializer, CommentSerializer, ReactionSerializer
from . models import Post, Comment, Reaction

class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    permission_classes = [AllowAny]
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        if serializer.is_valid():
            instance = serializer.save()
            Reaction.objects.create(post=instance)
    

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
    permission_classes = [AllowAny]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs['pk'])

    def get_object(self):
        return Post.objects.get(id=self.kwargs['pk'])
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(post=self.get_object())

class ReactAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ReactionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Reaction.objects.filter(post=self.get_object())
    
    def get_object(self):
        return Post.objects.get(id=self.kwargs['pk'])
    
    def perform_update(self, serializer):
        if serializer.is_valid():
            serializer.save()
            instance = Reaction.objects.get(post=self.get_object())
            instance.likes = serializer.data['likes']
            instance.dislikes = serializer.data['dislikes']
            instance.save()
            print(serializer.data['likes'])
            print(Reaction.objects.get(post=self.get_object()).likes)
        else:
            print(serializer.error)