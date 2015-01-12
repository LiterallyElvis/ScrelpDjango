from django import forms


class LoginForm(forms.Form):
    user_email = forms.EmailField
    password = forms.CharField(widget=forms.PasswordInput())


class RegistrationForm(forms.Form):
    user_email = forms.EmailField
    password = forms.CharField(widget=forms.PasswordInput())
    password_verify = forms.CharField(widget=forms.PasswordInput())
