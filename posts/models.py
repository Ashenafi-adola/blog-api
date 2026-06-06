from django.db import models
from datetime import datetime

class Post(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/images/', null=True, blank=True)
    description = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:20]

    
class Reaction(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    