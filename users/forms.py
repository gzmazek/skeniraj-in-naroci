from django import forms
from django.core.exceptions import ValidationError
import data.database as db
import hashlib

class RegistrationForm(forms.Form):
    email = forms.CharField(max_length=150)
    name = forms.CharField(max_length=150)
    surname = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    repeatPassword = forms.CharField(widget=forms.PasswordInput)
    termsAndConditions = forms.BooleanField()

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        repeatPassword = cleaned_data.get('repeatPassword')
        email = cleaned_data.get('email')

        if db.getUserByEmail(email) is not None:
            raise ValidationError("Email already in use")

        if password and repeatPassword and password != repeatPassword:
            raise ValidationError("Passwords do not match")
        
        return cleaned_data

class SignInForm(forms.Form):
    email = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        email = cleaned_data.get('email')

        user =  db.getUserByEmail(email) # gets user from database

        if user is None:
            raise ValidationError("Email or password is incorrect")
        else:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if hashed_password != user.password:
                raise ValidationError("Email or password is incorrect")

        return cleaned_data