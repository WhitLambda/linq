# api in json <-> web app in python
from rest_framework import serializers
from .models import Comments

class YTCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'