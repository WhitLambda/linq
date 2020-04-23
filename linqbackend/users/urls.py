from django.urls import path
from django.contrib.auth import views as auth_views

from .views import user_view, login_view, signup_view

urlpatterns = [
    path('', user_view.as_view(), name='user_view'),
    path('signup/', signup_view.as_view(), name='signup'),
    path('login/', login_view.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]