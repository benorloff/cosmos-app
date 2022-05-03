from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:user_id>/add_photo', views.add_photo, name='add_photo'),
    path('events/', views.EventList.as_view(), name='events_list'),
    path('events/create/', views.EventCreate.as_view(), name='events_create'),
    path('events/<int:pk>/', views.EventDetail.as_view(), name='events_detail'),
    path('events/<int:user_id>', views.add_watchlist, name='events_watchlist'),
    path('events/<int:pk>/update/', views.EventUpdate.as_view(), name='events_update'),
    path('parties/', views.PartyList.as_view(), name='parties_list'),
    path('parties/create/', views.PartyCreate.as_view(), name='parties_create'),
    path('parties/<int:pk>/', views.PartyDetail.as_view(), name='parties_detail'),
    # path('events/<int:pk>/update/', views.EventUpdate.as_view(), name='events_update'),
]