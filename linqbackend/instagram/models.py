from django.db import models

class Instagram_Comments(models.Model):
    username = models.CharField(max_length=100)
    message = models.CharField(max_length=2200)