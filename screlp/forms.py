# -*- coding: utf-8 -*- 

from django import forms
from screlp.models import ScrelpUser


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'parameters'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'parameters'}))


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'email@example.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'•••••••••••••••••••••••••'}))
    password_verify = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'verify password'}))

    class Meta:
        model = ScrelpUser
        fields = ("email", "password", "password_verify")


    def clean_password2(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password_verify")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2


    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

