from .models import UserComments
from django import forms


class UserCommentsForm(forms.ModelForm):
    class Meta:
        model = UserComments
        fields = ['text', 'rate']

    def __init__(self, *args, **kwargs):
        super(UserCommentsForm, self).__init__(*args, **kwargs)
        self.fields['rate'].required = False




