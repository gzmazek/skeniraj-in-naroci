from django import forms

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    name = forms.CharField(max_length=150, required=False)
    password = forms.CharField(widget=forms.PasswordInput)
    gender = forms.CharField(max_length=10, required=False)
