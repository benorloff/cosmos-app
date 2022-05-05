from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='users_detail'),
    path('users/update/', views.profile, name='users_update'),
    path('users/update/add_photo', views.add_profile_photo, name='add_profile_photo'),
    path('users/update/delete_photo', views.delete_profile_photo, name='delete_profile_photo'),
    path('events/', views.EventList.as_view(), name='events_list'),
    path('events/create/', views.EventCreate.as_view(), name='events_create'),
    path('events/<int:pk>/', views.EventDetail.as_view(), name='events_detail'),
    path('events/<int:event_id>', views.add_watchlist, name='events_watchlist'),
    path('events/<int:event_id>/remove', views.remove_watchlist, name='events_watchlistremove'),
    path('events/<int:pk>/update/', views.EventUpdate.as_view(), name='events_update'),
    path('events/<int:event_id>/update/add_photo', views.add_event_photo, name='add_event_photo'),
    path('events/<int:event_id>/update/delete_photo', views.delete_event_photo, name='delete_event_photo'),
    path('parties/', views.PartyList.as_view(), name='parties_list'),
    path('parties/create/', views.PartyCreate.as_view(), name='parties_create'),
    path('parties/<int:pk>/', views.PartyDetail.as_view(), name='parties_detail'),
    path('parties/<int:pk>/update/', views.PartyUpdate.as_view(), name='parties_update'),
    path('parties/<int:viewingparty_id>/add_attendee/', views.add_attendee, name='parties_add_attendee'),
    path('parties/<int:viewingparty_id>/remove_attendee/', views.remove_attendee, name='parties_remove_attendee'),
    # path('events/<int:pk>/update/', views.EventUpdate.as_view(), name='events_update'),
]