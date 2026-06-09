from rest_framework import serializers
from . models import Post, Comment, Like, Dislike, Views

class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField() 
    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = {'user':{'read_only':True}}


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Comment
        fields = "__all__"
        extra_kwargs = {'user':{'read_only':True}, 'post':{'read_only':True}}

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['post', 'user']

class DislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dislike
        fields = ['post', 'user']

class ViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Views
        fields = "__all__"
        extra_kwargs = {'user':{'read_only':True}, 'post':{'read_only':True}}