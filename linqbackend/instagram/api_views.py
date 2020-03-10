from rest_framework import viewsets
from . import models
from . import serializers

class IGCommentsViewset(viewsets.ModelViewSet):
        queryset = models.Instagram_Comments.objects.all()
        serializer_class = serializers.IGCommentsSerializer

