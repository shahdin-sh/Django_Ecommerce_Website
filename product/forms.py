from .models import UserComments
from django import forms
from accounts.models import CustomUserModel
from django.contrib import messages


class UserCommentsForm(forms.ModelForm):
    class Meta:
        model = UserComments
        fields = ['text', 'rate']

    def __init__(self, *args, **kwargs):
        super(UserCommentsForm, self).__init__(*args, **kwargs)
        self.fields['rate'].required = False


class GuestCommentForm(forms.ModelForm):
    class Meta:
        model = UserComments
        fields = ['name', 'email', 'text', 'rate']

    # def __init__(self, request, *args, **kwargs):
    #     super(GuestCommentForm, self).__init__(*args, **kwargs)
    #     if self.fields['name'] and self.fields['email'] in request.session['guest_data']:
    #         self.fields['name'].initial = request.session['guest_data']['name']
    #         self.fields['email'].initial = request.session['guest_data']['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUserModel.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('this email has been given before')
        else:
            return email


