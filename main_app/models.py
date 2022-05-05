from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    event_type = models.CharField(max_length=100)
    start_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    start_time = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    end_date = models.DateField(auto_now=False, auto_now_add=False, null=True)   
    end_time = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    best_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)   
    best_time = models.TimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    has_party = models.BooleanField(default=False)
    description = models.CharField(max_length=1200)
    users_watching = models.ManyToManyField(User, related_name='users_watching_event')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_created_by_user')

    def __str__(self):
        return f"Event is {self.title} in {self.location}."

    def get_absolute_url(self):
        return reverse('events_detail', kwargs={'pk': self.id})
    
class Profile(models.Model):
    photo_url = models.CharField(max_length=255, blank=True)
    birthdate = models.DateField(auto_now=False, auto_now_add=False, null=True)
    google_id = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    bio = models.CharField(max_length=500, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"This is the profile of {self.user}"

class ViewingParty(models.Model):
    name = models.CharField(max_length=100)
    party_location = models.CharField(max_length=100)    
    start_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    start_time = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    end_date = models.DateField(auto_now=False, auto_now_add=False, null=True)   
    end_time = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='party_created_by_user')
    description = models.CharField(max_length=500)
    attendees = models.ManyToManyField(User, related_name='party_attendees')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_viewing_party')

    def __str__(self):
        return f"Viewing party is {self.name}."

    def get_absolute_url(self):
        return reverse('parties_detail', kwargs={'pk': self.id})

class Photo(models.Model):
    url = models.CharField(max_length=255)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    party = models.ForeignKey(ViewingParty, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Photo at {self.url}"