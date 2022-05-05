from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import Lower
import uuid
import boto3
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
from .forms import UpdateUserForm, UpdateProfileForm

from .models import Event, ViewingParty, Profile, Photo, User

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'cosmos-app'
NASA_API = str(os.getenv('NASA_API'))
MAPBOX_API = str(os.getenv('MAPBOX_API'))
# Create your views here.

def home(request):
    data = requests.get(f'https://api.nasa.gov/planetary/apod?api_key={NASA_API}').text
    converted_data = json.loads(data)
    url = converted_data['url']
    events = Event.objects.order_by('users_watching')[:6]
    parties = ViewingParty.objects.order_by('attendees')[:3]
    return render(request, 'home.html', {'url': url, 'events': events, 'parties': parties})

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
        user = User.objects.get(id=request.user.id)
        profile = Profile.objects.get(id=user.profile.id)

        try:
          photo = Photo.objects.get(profile=profile.id)

          return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form, 'photo_url': photo.url, 'photo': photo, 'profile': profile})
        except:
          print('no photo is added')
          return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form, 'photo': False})

class UserDetail(DetailView):
  model = User
  fields = '__all__'
  
  def get_context_data(self, **kwargs):
    context = super(UserDetail, self).get_context_data(**kwargs)
    context['events'] = Event.objects.filter(users_watching=self.get_object())
    context['parties'] = ViewingParty.objects.filter(attendees=self.get_object())
    context['profile'] = Profile.objects.get(user=self.get_object())
    print(self.request.user)
    print(self.object)
    try:
      profile = Profile.objects.get(user=self.get_object())
      context['photo'] = Photo.objects.get(profile=profile.id)
    except:
      print('no user photo')
      context['photo'] = False
    return context

class UserUpdate(LoginRequiredMixin, UpdateView):
  model = User
  fields = ['username', 'email', 'first_name', 'last_name']

class EventList(ListView):
    model = Event
    paginate_by = 50

    def get_queryset(self):
      order = self.request.GET.get('orderby', 'start_date')
      if order == 'name':
        new_context = Event.objects.order_by(Lower(order))
      else:
        new_context = Event.objects.order_by(order)
      return new_context

    def get_context_data(self, **kwargs):
      context = super(EventList, self).get_context_data(**kwargs)
      context['orderby'] = self.request.GET.get('orderby', 'start_date')
      return context

class EventDetail(DetailView):
    model = Event
    fields =  ['title', 'location', 'event_type', 'start_date', 'start_time', 'end_date', 'end_time', 'best_date', 'best_time', 'description', 'users_watching', 'created_by']

    def get_context_data(self, **kwargs):
        context = super(EventDetail, self).get_context_data(**kwargs)
        context['parties'] = ViewingParty.objects.filter(event=self.get_object())
        try:
          photo = Photo.objects.get(event=self.get_object())
          context['photo'] = photo
          print(photo)
        except:
          print('no photo')
        return context

class EventCreate(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['title', 'location', 'event_type', 'start_date', 'start_time', 'end_date', 'end_time', 'best_date', 'best_time', 'description']
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class EventUpdate(LoginRequiredMixin, UpdateView):
    model = Event
    fields = ['title', 'location', 'event_type', 'start_date', 'start_time', 'end_date', 'end_time', 'best_date', 'best_time', 'description']

    def get_context_data(self, **kwargs):
      context = super(EventUpdate, self).get_context_data(**kwargs)
      try:
          photo = Photo.objects.get(event=self.get_object())
          print(photo.event)
          # if (photo.event == None):
          #   print('no event')
          # else:  
          #   context['photo'] = photo
          
      except:
        print('no photo')
      return context


class PartyList(ListView):
  model = ViewingParty
  paginate_by = 20

  def get_queryset(self):
    order = self.request.GET.get('orderby', 'start_date')
    if order == 'name':
      new_context = ViewingParty.objects.order_by(Lower(order))
    else:
      new_context = ViewingParty.objects.order_by(order)
    return new_context

  def get_context_data(self, **kwargs):
    context = super(PartyList, self).get_context_data(**kwargs)
    context['orderby'] = self.request.GET.get('orderby', 'start_date')
    context['mapbox_api'] = MAPBOX_API
    party_locations = ViewingParty.objects.all().values_list('party_location')
    geo_request_list = []
    for location in party_locations: 
      geo_request = requests.get('https://api.mapbox.com/geocoding/v5/mapbox.places/<str:location>.json')
      geo_request_list.append(geo_request)
    context['party_locations'] = geo_request_list
    print(geo_request_list)
    return context

class PartyDetail(DetailView):
  model = ViewingParty
  fields = '__all__'

class PartyCreate(LoginRequiredMixin, CreateView):
  model = ViewingParty
  fields = ['name', 'party_location', 'start_date', 'start_time', 'end_date', 'end_time', 'description', 'event']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

  def get_context_data(self, **kwargs):
    context = super(PartyCreate, self).get_context_data(**kwargs)
    context['mapbox_api'] = MAPBOX_API
    return context

class PartyUpdate(LoginRequiredMixin, UpdateView):
  model = ViewingParty
  fields = ['name', 'party_location', 'start_date', 'start_time', 'end_date', 'end_time', 'description']

def add_profile_photo (request):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]

    try:
        s3.upload_fileobj(photo_file, BUCKET, key)
        url = f"{S3_BASE_URL}{BUCKET}/{key}"
        # user = request.user
        profile = request.user.profile
        Photo.objects.create(url=url, profile=profile)
        
    except:
        print('An error occurred uploading file to S3')
    return redirect('users_update')

def delete_profile_photo (request):
  photo = Photo.objects.get(profile=request.user.profile)
  photo.profile = None
  photo.save()
  return redirect('users_update')

@login_required
def add_event_photo(request, event_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]

    try:
        s3.upload_fileobj(photo_file, BUCKET, key)
        url = f"{S3_BASE_URL}{BUCKET}/{key}"
        
        # print(request.event)
        event = Event.objects.get(id=event_id)
        Photo.objects.create(url=url, event=event)
    except:
        print('An error occurred uploading file to S3')

    return redirect('events_list')

def delete_event_photo (request, event_id):
  photo = Photo.objects.get(id=event_id)
  # photo.event = None
  # photo.save()
  print(photo.event)
  return redirect('events_list')    

@login_required
def add_watchlist (request, event_id):
  user = User.objects.get(id=request.user.id)
  event = Event.objects.get(id=event_id)
  try:
    event.users_watching.add(user)
    next = request.POST.get('next', '/')
  except:
    print('error adding user to event')

  return HttpResponseRedirect(next)

@login_required
def remove_watchlist (request, event_id):
  user = User.objects.get(id=request.user.id)
  event = Event.objects.get(id=event_id)
  try:
    event.users_watching.remove(user)
    next = request.POST.get('next', '/')
  except:
    print('error removing user to event')
  
  return HttpResponseRedirect(next)

@login_required
def add_attendee (request, viewingparty_id):
  user = User.objects.get(id=request.user.id)
  party = ViewingParty.objects.get(id=viewingparty_id)
  try:
    party.attendees.add(user)
    party.save()
    next = request.POST.get('next', '/')
  except:
    print('error adding attendee to viewing party')

  return HttpResponseRedirect(next)

@login_required
def remove_attendee (request, viewingparty_id):
  user = User.objects.get(id=request.user.id)
  party = ViewingParty.objects.get(id=viewingparty_id)
  try:
    party.attendees.remove(user)
    party.save()
    next = request.POST.get('next', '/')
  except:
    print('error removing attendee to viewing party')

  return HttpResponseRedirect(next)
