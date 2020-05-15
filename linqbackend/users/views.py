from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response

import json
import pprint

from .models import users, user_socials, user_medias, user_keywords
from instagram.models import Comments as ig_comments
from youtube.models import Comments as yt_comments
from twitch.models import Comments as twitch_comments
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









# HAVE THIS AS THE FETCH IN REACT FRONTEND       MAKE IT A POST REQUEST AND PROVIDE THE USERNAME AND PASSWORD

# fetch("http://127.0.0.1:8000/users/reacttest/",
#     {
#         method: 'POST',
#         body: JSON.stringify({'username': 'fff3', 'password': 'fff3'})
#     })
#     .then(res => res.json())
#     .then(
#     (result) => {
#         this.setState({
#             isLoaded: true,
#             comments: result.comments
#         });
#     ...

# IT'S MAKING A POST REQUEST BUT THAT IS NEEDED TO SEND DATA (username, password) TO GET keywords/comments FROM THE DATABASE

class get_keywords_view(APIView):
    def get(self, request): 
        pass
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        # password = data['password']
        # user = authenticate(request, username='fff3', password='fff3')
        # login(request, user)

        # if request.user.is_authenticated:
        response_body = {}
        for p in User.objects.filter(username=username):     # username should be unique so it should loop only once
            response_body['username'] = p.username
            response_body['email'] = p.email
            response_body['success'] = 'true'

        response_body['keywords'] = []
        for k in user_keywords.objects.filter(linq_username=username):
            kwd = {
                'keyword': k.keyword,
                'responses': [r for r in k.responses.split(' @@@ ')],
                'autoreply': k.autoreply
            }
            response_body['keywords'].append( kwd )
        # no keywords yet :(
        
        return Response( response_body )

        # else:
        #     return Response( {"success": "false"} )

class get_comments_view(APIView):
    def get(self, request):
        pass
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        # password = data['password']
        # user = authenticate(request, username='fff3', password='fff3')
        # login(request, user)

        # if request.user.is_authenticated:
        response_body = {}
        for p in User.objects.filter(username=username):    # username should be unique so it should loop only once
            response_body['username'] = p.username
            response_body['email'] = p.email
            response_body['success'] = 'true'

        response_body['comments'] = []
        for igc in ig_comments.objects.filter(username=username):
            response_body['comments'].append( 
                {
                    "username": igc.username,
                    "timestamp": "2020-01-22 22:19:46",
                    "commentId": "1234567890",
                    "commentText": igc.message,
                    "keywords": [],
                    "platform": "instagram",
                    "mediaId": "11111"
                }
            )
        for ytc in yt_comments.objects.filter(linq_username=username):
            response_body['comments'].append( 
                {
                    "username": ytc.linq_username,
                    "timestamp": ytc.timestamp,
                    "commentId": ytc.comment_Id,
                    "commentText": ytc.message,
                    "keywords": [],
                    "platform": "youtube",
                    "mediaId": ytc.video_id
                }
            )
        for tc in twitch_comments.objects.filter(linq_username=username):
            response_body['comments'].append(
                {
                    "username": tc.linq_username,
                    "timestamp": tc.timestamp,
                    "commetText": tc.message,
                    "keywords": [],
                    "platform": "twitch",
                    "mediaId": "11111"
                }
            )
        pprint.pprint(response_body)
        return Response( response_body )

        # else:
        #     return Response( {"success": "false"} )

















class get_keywords_test_view(APIView):
    def get(self, request):
        # get current user and the keywords for that user in the database
        return Response(
            {
                "username": "some_user",
                "keywords": [
                    {
                        "keyword": "stream schedule",
                        "responses": [
                            "I'm streaming MWF at 10am",
                            "I stream 3 times a week"
                        ],
                        "autoreply": "true"
                    },
                    {
                        "keyword": "nice video",
                        "responses": [
                            "Thanks!",
                            "Thank you!"
                        ],
                        "autoreply": "true"
                    },
                    {
                        "keyword": "how are you",
                        "responses": [
                            "Doing well thanks!",
                            "I'm great, how are you?"
                        ],
                        "autoreply": "true"
                    }
                ]
            }
        )
    def post(self, request):
        pass

class get_comments_test_view(APIView):
    def get(self, request):
        # get current user and return all their comments
        return Response(
            {
                "comments": [
                    {
                        "username": "xXdr4g0n_sl4y3rXx",
                        "timestamp": "2020-01-22 22:19:46",
                        "commentId": "1234567890",
                        "commentText": "hey what is your streaming schedule? aaaaaaaaaaaaaaa",
                        "keywords": [
                            "streaming schedule"
                        ],
                        "platform": "twitter",
                        "mediaId": "0987654321"
                    },
                    {
                        "username": "fan_of_urs123",
                        "timestamp": "2020-01-11 11:21:45",
                        "commentId": "1234567890",
                        "commentText": "this was a great video! aaaaaaaaaaaa",
                        "keywords": [
                            "great video"
                        ],
                        "platform": "youtube",
                        "mediaId": "0987654321"
                    },
                    {
                        "username": "catzilla",
                        "timestamp": "2020-02-08 19:06:31",
                        "commentId": "1234567890",
                        "commentText": "Where did you get that food? aaaaaaaaaaaaaaaaa",
                        "keywords": [],
                        "platform": "twitch",
                        "mediaId": "0987654321"
                    },
                ]
            }
        )
    def post(self, request):
        return Response(
            {
                "comments": [
                    {
                        "username": "xXdr4g0n_sl4y3rXx",
                        "timestamp": "2020-01-22 22:19:46",
                        "commentId": "1234567890",
                        "commentText": "hey what is your streaming schedule? aaaaaaaaaaaaaaa",
                        "keywords": [
                            "streaming schedule"
                        ],
                        "platform": "twitter",
                        "mediaId": "0987654321"
                    },
                    {
                        "username": "fan_of_urs123",
                        "timestamp": "2020-01-11 11:21:45",
                        "commentId": "1234567890",
                        "commentText": "this was a great video! aaaaaaaaaaaa",
                        "keywords": [
                            "great video"
                        ],
                        "platform": "youtube",
                        "mediaId": "0987654321"
                    },
                    {
                        "username": "catzilla",
                        "timestamp": "2020-02-08 19:06:31",
                        "commentId": "1234567890",
                        "commentText": "Where did you get that food? aaaaaaaaaaaaaaaaa",
                        "keywords": [],
                        "platform": "twitch",
                        "mediaId": "0987654321"
                    },
                ]
            }
        )
