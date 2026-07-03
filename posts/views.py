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

    def get_object(self):
        view = Views.objects.get(post=self.kwargs['pk'])
        try:
            if self.request.user not in view.user.all():
                view.user.add(self.request.user)
        except:
            pass
        return Post.objects.get(id=self.kwargs['pk'])

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
        user_id = self.reuest.user.id
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

    http_method_names = ['like', 'dislike']

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

class LikeAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Like.objects.all()
    
    def get_object(self):
        post = Post.objects.get(id=self.kwargs['pk'])
        instance, created = Like.objects.get_or_create(post=post)
        return instance

    def put(self, request, *args, **kwargs):
        userId = self.request.user.id
        users = self.request.data['user']
        post = Post.objects.get(id=self.kwargs['pk'])
        dislike = Dislike.objects.get(post=post)

        if userId in users:
            users.remove(userId)
            self.request.data['user'] = users
        else:
            users.append(userId)
            self.request.data['user'] = users
        
        serializer = LikeSerializer(
            Like.objects.get(post=post),
            data= self.request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            if self.request.user in dislike.user.all():
                dislike.user.remove(self.request.user)
            print("saved")
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    def perform_update(self, serializer):
        serializer.save()

class DisLikeAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = DislikeSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Dislike.objects.all()
    
    def get_object(self):
        post = Post.objects.get(id=self.kwargs['pk'])
        instance, created = Dislike.objects.get_or_create(post=post)
        return instance

    def put(self, request, *args, **kwargs):
        userId = self.request.user.id
        users = self.request.data['user']
        post = Post.objects.get(id=self.kwargs['pk'])
        like = Like.objects.get(post=post)

        if userId in users:
            users.remove(userId)
            self.request.data['user'] = users
        else:
            users.append(userId)
            self.request.data['user'] = users
        
        serializer = LikeSerializer(
            Dislike.objects.get(post=post),
            data= self.request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            if self.request.user in like.user.all():
                like.user.remove(self.request.user)
            print("saved")
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    def perform_update(self, serializer):
        serializer.save()

class ViewsAPIView(generics.RetrieveAPIView):
    serializer_class = ViewsSerializer
    permission_classes = [AllowAny]
    queryset = Views.objects.all()

    def get_object(self):
        post = Post.objects.get(id=self.kwargs['pk'])
        return Views.objects.get(post=post)