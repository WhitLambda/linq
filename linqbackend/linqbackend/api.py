from rest_framework import routers
from instagram.api_views import IGCommentsViewset
from youtube.api_views import YTCommentsViewset

router = routers.DefaultRouter()
router.register(r'instagram_comments', IGCommentsViewset)
router.register(r'youtube_comments', YTCommentsViewset)