from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)     # https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone

    def __str__(self):
        return self.user

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        users.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.users.save()



class user_keywords(models.Model):
    linq_username = models.CharField(max_length=100)
    keyword = models.CharField(max_length=500)
    responses = models.TextField(blank=True)
    autoreply = models.CharField(max_length=100)




class user_socials(models.Model):
    # primary key automatically generated as auto-integer field
    platform = models.CharField(max_length=200)
    social_username = models.CharField(max_length=200)
    access_token = models.TextField(blank=True)
    linq_user = models.ForeignKey(users, on_delete=models.CASCADE, null=True)
    social_active = models.BooleanField(default=False)

    class Meta:
        unique_together = ('platform', 'social_username')

    def __str__(self):
        return self.social_username


class user_medias(models.Model):
    # primary key automatically generated as auto-integer field
    platform = models.CharField(max_length=200)
    media_id = models.TextField()
    social_account = models.ForeignKey(user_socials, on_delete=models.CASCADE, null=True)
    media_active = models.BooleanField(default=False)

    class Meta:
        unique_together = ('platform', 'media_id')

    def __str__(self):
        return self.media_id
