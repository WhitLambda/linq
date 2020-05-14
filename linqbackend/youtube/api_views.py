from rest_framework import viewsets
from . import models
from . import serializers

class YoutubeCommentsViewset(viewsets.ModelViewSet):
    queryset = models.Comments.objects.all()
    serializer_class = serializers.YTCommentsSerializer