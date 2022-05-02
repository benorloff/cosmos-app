from django import forms

from.django.contrib.auth.models import User
from .models import Profile

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']

class UpdateProfileForm(forms.ModelForm):
    bio = forms.CharField(max_length=500)
    city = forms.CharField(max_length=50)
    birthdate = forms.DateField(auto_now=False, auto_now_add=False)

    class Meta:
        model = Profile
        fields = ['bio', 'city', 'birthdate']

