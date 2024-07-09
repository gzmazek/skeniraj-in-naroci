from django import forms

class AddRestaurantForm(forms.Form):
    name = forms.CharField(max_length=150)
    address = forms.CharField(max_length=255)