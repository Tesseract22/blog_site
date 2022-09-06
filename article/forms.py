from django import forms

from pagedown.widgets import AdminPagedownWidget

from .models import Article

class AlbumForm(forms.ModelForm):
    body = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = Article
        fields = "__all__"