from rest_framework import serializers
from .models import Comments

class TwitchCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'