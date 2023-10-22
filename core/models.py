from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    id_user = models.IntegerField()
    bio = models.TextField(max_length=500, blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank_picture.png')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username
