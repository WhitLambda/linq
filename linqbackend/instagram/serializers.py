from rest_framework import serializers
from . import models

class IGCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Instagram_Comments
        fields = ('username', 'message')