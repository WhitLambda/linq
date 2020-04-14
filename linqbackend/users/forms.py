from django import forms
from django.contrib.auth.models import User
# from .models import users

class signup_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')


class login_form(forms.Form):
    username = forms.CharField(label='Username', max_length=200)
    password = forms.CharField(label='Password', max_length=200)