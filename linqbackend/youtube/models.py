from django.db import models

class Comments(models.Model):
    comment_Id = models.CharField(max_length=100)
    linq_username = models.CharField(max_length=100)
    message = models.CharField(max_length=2200)
    YT_username = models.CharField(max_length=100)
    YT_userId = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    video_id = models.CharField(max_length=100)
    