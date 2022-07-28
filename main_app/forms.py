# from multiprocessing import Event
from django import forms

from django.contrib.auth.models import User
from .models import Profile, Event

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class UpdateProfileForm(forms.ModelForm):
    bio = forms.CharField(label='Bio', max_length=500, required=False)
    city = forms.CharField(label='City', max_length=50, required=False)
    birthdate = forms.DateField(label='Birthdate', required=False)

    class Meta:
        model = Profile
        fields = ['bio', 'city', 'birthdate']

class EventCreateForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(EventCreateForm, self).clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if end_date <= start_date:
            raise forms.ValidationError("End date must be later than start date")

        return cleaned_data

    class Meta:
        model = Event
        fields = ['title', 'location', 'event_type', 'start_date', 'start_time', 'end_date', 'end_time', 'best_date', 'best_time', 'description']

