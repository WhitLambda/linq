from rest_framework import routers
from instagram.api_views import InstagramCommentsViewset
from youtube.api_views import YoutubeCommentsViewset
from twitch.api_views import TwitchCommentsViewset

router = routers.DefaultRouter()
router.register(r'youtube_comments', YoutubeCommentsViewset, basename='youtube')
router.register(r'instagram_comments', InstagramCommentsViewset, basename='instagram')
router.register(r'twitch_comments', TwitchCommentsViewset, basename='twitch')