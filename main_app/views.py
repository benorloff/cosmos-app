from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3

from .forms import UpdateUserForm, UpdateProfileForm

from .models import Event, ViewingParty, Profile, Photo, User

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'cosmos-app'

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
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form})

class EventList(ListView):
    model = Event

class EventDetail(DetailView):
    model = Event
    fields =  ['title', 'location', 'event_type', 'start_date', 'start_time', 'end_date', 'end_time', 'description', 'users_watching', 'created_by']

class EventCreate(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['title', 'location', 'event_type', 'start_date', 'start_time', 'end_date', 'end_time', 'description']
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class EventUpdate(LoginRequiredMixin, UpdateView):
    model = Event
    fields = ['title', 'location', 'event_type', 'start_date', 'start_time', 'end_date', 'end_time', 'description']

class PartyList(ListView):
  model = ViewingParty

class PartyDetail(DetailView):
  model = ViewingParty
  fields = '__all__'

class PartyCreate(LoginRequiredMixin, CreateView):
  model = ViewingParty
  fields = ['name', 'party_location', 'start_date', 'start_time', 'end_date', 'end_time', 'description']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class PartyUpdate(LoginRequiredMixin, UpdateView):
  model = ViewingParty
  fields = ['name', 'party_location', 'start_date', 'start_time', 'end_date', 'end_time', 'description']

def add_photo (request, user_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]

    try:
        s3.upload_fileobj(photo_file, BUCKET, key)
        # build the full url string
        url = f"{S3_BASE_URL}{BUCKET}/{key}"
        # we can assign to cat_id or cat (if you have a cat object)
        user = User.objects.get(id=user_id)
        profile = Profile.objects.get(id=user.profile.id)
        Photo.objects.create(url=url, profile=profile)
        
    except:
        print('An error occurred uploading file to S3')
    return redirect('profile')

def add_watchlist (request, event_id):
  user = User.objects.get(id=request.user.id)
  event = Event.objects.get(id=event_id)
  try:
    event.users_watching.add(user)
  except:
    print('error adding user to event')

  return redirect('events_detail', pk=event_id)

def remove_watchlist (request, event_id):
  user = User.objects.get(id=request.user.id)
  event = Event.objects.get(id=event_id)
  try:
    event.users_watching.remove(user)
  except:
    print('error removing user to event')
  
  return redirect('events_detail', pk=event_id)