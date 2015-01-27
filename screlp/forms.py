from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    user_email = forms.EmailField(widget=forms.TextInput(attrs={'class':'parameters'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'parameters'}))


#class RegistrationForm(forms.ModelForm):
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class':'parameters'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class':'parameters'}))
    verify_password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class':'parameters'}))
