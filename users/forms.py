from django import forms

class RegistrationForm(forms.Form):
    email = forms.CharField(max_length=150)
    name = forms.CharField(max_length=150)
    surname = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    repeatPassword = forms.CharField(widget=forms.PasswordInput)
    termsAndConditions = forms.BooleanField()

class SignInForm(forms.Form):
    email = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False)

class ChangePasswordForm(forms.Form):
    oldPass = forms.CharField(widget=forms.PasswordInput)
    newPass = forms.CharField(widget=forms.PasswordInput)
    newPassRep = forms.CharField(widget=forms.PasswordInput)