from django import forms
from .models import Url

class FnewUrl(forms.ModelForm):
    class Meta:
        model = Url
        fields =('url',)