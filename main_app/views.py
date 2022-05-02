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

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

@login_required
def profile(request):
    return render(request, 'profile.html')

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
