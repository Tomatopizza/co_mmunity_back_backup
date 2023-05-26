from django.db import models
from users. models import MyUser
# Create your models here.

class Articles(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(MyUser, blank=True, related_name="article")

class Comments(models.Model):
    article = models.ForeignKey(Articles, on_delete=models.CASCADE, related_name='comment')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

