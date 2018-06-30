from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class Requestform(forms.Form):

    AND = 'AND'
    OR = 'OR'
    NOT = '-'
    NONE='NONE'
    options = (
        (NONE, 'NONE'),
        (OR, 'OR'),
        (NOT, 'NOT'),
        (AND,'AND')
    )
    Topicname = forms.CharField(max_length=100)
    input2 = forms.CharField(required=False)
    option2 = forms.ChoiceField(choices=options,required=False)
    input3 = forms.CharField(required=False)
    option3 = forms.ChoiceField(choices=options,required=False)
    input4 = forms.CharField(required=False)
    option4 = forms.ChoiceField(choices=options,required=False)
    input5 = forms.CharField(required=False)
    option5 = forms.ChoiceField(choices=options,required=False)
    input6 = forms.CharField(required=False)