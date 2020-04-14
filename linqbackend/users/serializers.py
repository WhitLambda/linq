from rest_framework import serializers

from .models import users, user_socials, user_medias

class user_serializer(serializers.ModelSerializer):
    class Meta:
        model = users
        fields = "__all__"          # or ['comment_id', 'linq_username', 'media_id', 'message']


class user_socials_serializer(serializers.ModelSerializer):
    class Meta:
        model = user_socials
        fields = "__all__"


class user_medias_serializer(serializers.ModelSerializer):
    class Meta:
        model = user_medias
        fields = "__all__"