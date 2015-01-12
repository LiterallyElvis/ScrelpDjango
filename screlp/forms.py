from django import forms


class LoginForm(forms.Form):
    user_email = forms.EmailField(widget=forms.TextInput(attrs={'class':'parameters'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'parameters'}))


class RegistrationForm(forms.Form):
    user_email = forms.EmailField(widget=forms.TextInput(attrs={'class':'parameters'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'parameters'}))
    password_verify = forms.CharField(widget=forms.PasswordInput(attrs={'class':'parameters'}))
