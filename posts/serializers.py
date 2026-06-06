from rest_framework import serializers
from . models import Post, Comment, Reaction

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text']

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ['post', 'likes', 'dislikes']
        extra_kwargs = {'post': {'read_only': True}}