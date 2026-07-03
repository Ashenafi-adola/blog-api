from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, DislikeSerializer, ViewsSerializer
from . models import Post, Comment, Like,Dislike, Views
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        if serializer.is_valid():
            instance = serializer.save(user=self.request.user)
            Like.objects.create(post=instance)
            Dislike.objects.create(post=instance)
            Views.objects.create(post=instance)
    

class PostUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [AllowAny]
    serializer_class = PostSerializer
    http_method_names = generics.RetrieveUpdateDestroyAPIView.http_method_names + ['like', "dislike"]

    def get_object(self):
        view = Views.objects.get(post=self.kwargs['pk'])
        try:
            if self.request.user not in view.user.all():
                view.user.add(self.request.user)
        except:
            pass
        return Post.objects.get(id=self.kwargs['pk'])
    
    def get(self, request, *args, **kwargs):
        likes = Like.objects.get(post=self.kwargs['pk']).user.all().count()
        dislikes = Dislike.objects.get(post=self.kwargs['pk']).user.all().count()
        views = Views.objects.get(post=self.kwargs['pk']).user.all().count()
        serializer = PostSerializer(self.get_object())
        return Response(
            {
                'likes': likes,
                'dislikes': dislikes,
                'views': views,
                'post': serializer.data
            }
        )

    def perform_update(self, serializer):
        if serializer.is_valid():
            serializer.save()

    def put(self, request, *args, **kwargs):
        
        serializer = PostSerializer(
            self.get_object(),
            data=request.data,
            partial=True
        )
        data = request.data.copy()

        if 'image' not in request.FILES:
            if type(data['image']) == str:
                data.pop('image')

        serializer = PostSerializer(
            self.get_object(),
            data=data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def like(self, request, *args, **kwargs):
        like = Like.objects.get(post=self.kwargs['pk'])
        likes = like.user.all()
        dislike = Dislike.objects.get(post=self.kwargs['pk'])
        dislikes = dislike.user.all()

        if self.request.user in likes:
            like.user.remove(self.request.user)
        else:
            like.user.add(self.request.user)
            if self.request.user in dislikes:
                dislike.user.remove(self.request.user)
        
        serializer = LikeSerializer(
            Like.objects.get(post=self.kwargs['pk']),
            data= self.request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.data
        )
    
    def dislike(self, request, *args, **kwargs):
        like = Like.objects.get(post=self.kwargs['pk'])
        likes = like.user.all()
        dislike = Dislike.objects.get(post=self.kwargs['pk'])
        dislikes = dislike.user.all()

        if self.request.user in dislikes:
            dislike.user.remove(self.request.user)
        else:
            dislike.user.add(self.request.user)
            if self.request.user in likes:
                like.user.remove(self.request.user)
        
        serializer = LikeSerializer(
            Like.objects.get(post=self.kwargs['pk']),
            data= self.request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.data
        )
        
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
    permission_classes = [AllowAny]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs['pk']).order_by('-commented_at')

    def get_object(self):
        return Post.objects.get(id=self.kwargs['pk'])
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(post=self.get_object(), user=self.request.user)

class EditDestroyCommentAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def get_object(self):
        return Comment.objects.get(id=self.kwargs['pk'])

    def perform_update(self, serializer):
        if serializer.is_valid():
            serializer.save()
        return super().perform_update(serializer)
    
    def put(self, request, *args, **kwargs):
        serializer = CommentSerializer(
            self.get_object(),
            data = request.data,
            partial=True
        )
        print('put method invoked')
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
