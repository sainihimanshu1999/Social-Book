from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    id_user = models.IntegerField()
    bio = models.TextField(max_length=500, blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank_picture.png')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username
    

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to = 'post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user+' -> '+self.caption
    


class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class FollowerCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.follower+' is following '+self.user