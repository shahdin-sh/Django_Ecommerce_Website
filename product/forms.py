from .models import UserComments
from django import forms


class UserCommentsForm(forms.ModelForm):
    class Meta:
        model = UserComments
        fields = ['text', 'rate']


