from django.urls import path
from django.contrib.auth import views as auth_views

from .views import user_view, login_view, signup_view
from .views import get_keywords_view, get_comments_view, get_keywords_test_view,  get_comments_test_view

urlpatterns = [
    path('', user_view.as_view(), name='user_view'),
    path('signup/', signup_view.as_view(), name='signup'),
    path('login/', login_view.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('getkeywords/', get_keywords_view.as_view(), name='get_keywords'),
    path('getcomments/', get_comments_view.as_view(), name='get_comments')

    path('gettestkeywords/', get_keywords_test_view.as_view(), name='get_keywords_test'),
    path('gettestcomments/', get_comments_test_view.as_view(), name='get_comments_test')
]