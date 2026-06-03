from rest_framework import serializers
from . models import Post, Comment

class PostSerializer(serializers.ModelField):
    class Meta:
        model = Post
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text']