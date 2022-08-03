from django import forms


class ItemForm(forms.Form):
    item = forms.CharField(label='item')