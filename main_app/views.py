from django.shortcuts import render, redirect

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3

from .models import Event, ViewingParty, Profile, Photo

# Create your views here.

def home(request):
  return render(request, 'home.html')

class EventList(ListView):
    model = Event

class EventDetail(DetailView):
    model = Event
    fields =  ['title', 'location', 'event_type', 'start_time', 'end_time', 'description', 'users_watching', 'created_by']

class EventCreate(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['title', 'location', 'event_type', 'start_time', 'end_time', 'description', 'created_by']
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class EventUpdate(LoginRequiredMixin, UpdateView):
    model = Event
    fields = ['title', 'location', 'event_type', 'start_time', 'end_time', 'description']
