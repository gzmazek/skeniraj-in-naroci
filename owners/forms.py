from django import forms
from data.model import Table


class AddRestaurantForm(forms.Form):
    name = forms.CharField(max_length=150)
    address = forms.CharField(max_length=255)

class TableForm(forms.Form):
    restaurant_id = forms.IntegerField(widget=forms.HiddenInput(), required=True)
    
class AddKitchenForm(forms.Form):
    name = forms.CharField(max_length=150)

class AddItemForm(forms.Form):
    name = forms.CharField(max_length=150)
    value = forms.DecimalField()
