from django.shortcuts import render, redirect

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

from .models import Event, ViewingParty, Profile, Photo

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
    fields =  ['title', 'location', 'event_type', 'start_time', 'end_time', 'description', 'users_watching', 'created_by']

class EventCreate(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['title', 'location', 'event_type', 'start_time', 'end_time', 'description']
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class EventUpdate(LoginRequiredMixin, UpdateView):
    model = Event
    fields = ['title', 'location', 'event_type', 'start_time', 'end_time', 'description']

def add_photo (request, profile_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]

    try:
        s3.upload_fileobj(photo_file, BUCKET, key)
        # build the full url string
        url = f"{S3_BASE_URL}{BUCKET}/{key}"
        # we can assign to cat_id or cat (if you have a cat object)
        Photo.objects.create(url=url, profile_id=profile_id)
        
    except:
        print('An error occurred uploading file to S3')
    return redirect('profile')

def add_watchlist (request, user_id):
  print('button is working')

  return redirect('profile')