from rest_framework import viewsets
from . import models
from . import serializers

class TwitchCommentsViewset(viewsets.ModelViewSet):
    queryset = models.Comments.objects.all()
    serializer_class = serializers.TwitchCommentsSerializer