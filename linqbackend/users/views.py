from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import users, user_socials, user_medias
from .serializers import user_serializer, user_socials_serializer, user_medias_serializer
from .forms import signup_form, login_form

# Create your views here.

class user_view(APIView):
    def get(self, request):
        return Response(
            {"message": "user_view get"}
        )

    def post(self, request):
        return Response({"message": "user_view post"})



class signup_view(APIView):
    def get(self, request):
        return render(request, 'signup.html', {'form': signup_form} )
    
    def post(self, request):
        # print('POSTPOSTPOST', request.POST)
        form = signup_form(request.POST)

        if form.is_valid():
            # user = form.save(commit=False)
            input_username = form.cleaned_data.get('username')     # https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
            input_password = form.cleaned_data.get('password')
            input_email = form.cleaned_data.get('email')
            user = User.objects.create(username=input_username, email=input_email)
            user.set_password(input_password)
            user.save()
            return redirect('login')
        else:
            return Response({
                "error": form.errors        # https://www.reddit.com/r/django/comments/7pklwd/why_formisvalid_always_returns_false_help/
            })


class login_view(APIView):
    def get(self, request):
        return render(request, 'login.html', {'form': login_form} )
    
    def post(self, request):
        # print('LOGINPOSTPOST', request.POST)
        form = login_form(request.POST)

        if form.is_valid():
            input_username = form.cleaned_data.get('username')
            input_password = form.cleaned_data.get('password')
            # print('\nusername:{} - pwd:{}'.format(input_username, input_password))
            user = authenticate(request, username=input_username, password=input_password)
            # print('LOGINUSERPOST', user)
            if user is not None:
                login(request, user)
                return redirect('user_view')
            else:
                return Response({"error": "unable to authenticate user"})
        else:
            return Response({
                "error": form.errors
            })