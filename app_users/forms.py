from django import forms

from django.contrib.auth.models import User
from app_users.models import user_profile
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):
    model = forms.EmailField()
    fields = (
        'username', 'first_name', 'last_name', 'email', 'password1', 'password2'
    )

    labels = {
        'password1':'Password',
        'password2':'Confirm Password'
    }

class UserProfileInfoForm(forms.ModelForm):
    bio = forms.CharField(required=False)

    teacher = 'teacher'
    student = 'student'
    parent = 'parent'

    user_types = [
        (student, 'student'),
        (parent, 'parent'),
    ]
    user_type = forms.ChoiceField(choices=user_types, required=True)

    class Meta():
        model = user_profile
        fields = ('bio', 'profile_Pic', 'user_type')
