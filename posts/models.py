from django.db import models
from accounts.models import Account
class Post(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    description = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.DO_NOTHING, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    commented_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.text[:20]

class Like(models.Model):
    user = models.ManyToManyField(Account, related_name='likes')
    post = models.OneToOneField(Post, on_delete=models.CASCADE)

class Dislike(models.Model):
    user = models.ManyToManyField(Account, related_name='dislikes')
    post = models.OneToOneField(Post, on_delete=models.CASCADE)

class Views(models.Model):
    user = models.ManyToManyField(Account, related_name='views')
    post = models.OneToOneField(Post, on_delete=models.CASCADE)