from rest_framework import routers
from instagram import api_views as myapp_views

router = routers.DefaultRouter()
router.register(r'instagram_comments', myapp_views.IGCommentsViewset)