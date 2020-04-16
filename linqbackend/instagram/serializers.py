from rest_framework import serializers
from .models import Comments

class IGCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('username', 'message')