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



# current username







class getkeywords_view(APIView):
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

# view for user data and keywords
# and also put request for updating user's keywords
## example:
    # {
    #     "username": "some_user",
    #     "keywords": [
    #         {
    #             "keyword": "stream schedule",
    #             "responses": [
    #                 "I'm streaming MWF at 10am",
    #                 "I stream 3 times a week"
    #             ],
    #             "autoreply": true
    #         },
    #         {
    #             "keyword": "nice video",
    #             "responses": [
    #                 "Thanks!",
    #                 "Thank you!"
    #             ],
    #             "autoreply": true
    #         },
    #         {
    #             "keyword": "how are you",
    #             "responses": [
    #                 "Doing well thanks!",
    #                 "I'm great, how are you?"
    #             ],
    #             "autoreply": true
    #         }
    #     ]
    # }






class getcomments_view(APIView):
    def get(self, request):
        # get current user and return all their comments
        print('getcomments get request made ...')

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
        pass

# example:
    # {
    # 	"comments": [
    # 		{
    # 			"username": "xXdr4g0n_sl4y3rXx",
    # 			"timestamp": "2020-01-22 22:19:46",
    # 			"commentId": "1234567890",
    # 			"commentText": "hey what is your streaming schedule?",
    # 			"keywords": [
    # 				"streaming schedule"
    # 			],
    # 			"platform": "twitter",
    # 			"mediaId": "0987654321"
    # 		},
    # 		{
    # 			"username": "fan_of_urs123",
    # 			"timestamp": "2020-01-11 11:21:45",
    # 			"commentId": "1234567890",
    # 			"commentText": "this was a great video!",
    # 			"keywords": [
    # 				"great video"
    # 			],
    # 			"platform": "youtube",
    # 			"mediaId": "0987654321"
    # 		},
    #     {
    # 			"username": "CopperCorgi",
    # 			"timestamp": "2020-04-03 23:58:20",
    # 			"commentId": "1234567890",
    # 			"commentText": "Your art is lame >:(",
    # 			"keywords": [],
    # 			"platform": "reddit",
    # 			"mediaId": "0987654321"
    # 		},
    # 		{
    # 			"username": "catzilla",
    # 			"timestamp": "2020-02-08 19:06:31",
    # 			"commentId": "1234567890",
    # 			"commentText": "Where did you get that food?",
    # 			"keywords": [],
    # 			"platform": "twitch",
    # 			"mediaId": "0987654321"
    # 		},
    # 		{
    # 			"username": "fan_of_urs123",
    # 			"timestamp": "2020-02-03 21:32:04",
    # 			"commentId": "1234567890",
    # 			"commentText": "like if you're part of the notification squad!!!",
    # 			"keywords": [
    # 				"notification squad"
    # 			],
    # 			"platform": "youtube",
    # 			"mediaId": "0987654321"
    # 		},
    # 		{
    # 			"username": "orangeyouglad",
    # 			"timestamp": "2020-02-27 00:23:37",
    # 			"commentId": "1234567890",
    # 			"commentText": "I like your cat",
    # 			"keywords": [],
    # 			"platform": "twitch",
    # 			"mediaId": "0987654321"
    # 		},
    # 		{
    # 			"username": "xXdr4g0n_sl4y3rXx",
    # 			"timestamp": "2020-03-22 16:01:23",
    # 			"commentId": "1234567890",
    # 			"commentText": "Where do we donate? This is a great video!",
    # 			"keywords": [
    # 				"donate",
    #         "great video"
    # 			],
    # 			"platform": "youtube",
    # 			"mediaId": "0987654321"
    # 		},
    # 		{
    # 			"username": "some_kinda_spam_guy",
    # 			"timestamp": "2020-02-22 13:15:52",
    # 			"commentId": "1234567890",
    # 			"commentText": "sub for sub?",
    # 			"keywords": [
    # 				"sub for sub"
    # 			],
    # 			"platform": "youtube",
    # 			"mediaId": "0987654321"
    # 		},
    # 		{
    # 			"username": "double_triple_quad234",
    # 			"timestamp": "2020-01-23 17:24:33",
    # 			"commentId": "1234567890",
    # 			"commentText": "Love this content! Can't wait for more!",
    # 			"keywords": [],
    # 			"platform": "twitter",
    # 			"mediaId": "0987654321"
    # 		},
    # 		{
    # 			"username": "xXdr4g0n_sl4y3rXx",
    # 			"timestamp": "2020-02-03 01:15:30",
    # 			"commentId": "1234567890",
    # 			"commentText": "omg I love you",
    # 			"keywords": [
    # 				"I love you"
    # 			],
    # 			"platform": "reddit",
    # 			"mediaId": "0987654321"
    # 		}
    # 	]
    # }
