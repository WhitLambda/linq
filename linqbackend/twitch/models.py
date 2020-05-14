from django.db import models

class Comments(models.Model):
    linq_username = models.CharField(max_length=100)
    message = models.CharField(max_length=2200)
    twitch_username = models.CharField(max_length=100)
    twitch_userId = models.CharField(max_length=100)
    timestamp = models.DateTimeField()