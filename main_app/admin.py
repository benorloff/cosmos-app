from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Event, Profile, Photo, ViewingParty

from import_export.admin import ImportExportMixin

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

class EventAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = [
        'title', 
        'location', 
        'event_type', 
        'start_date', 
        'start_time', 
        'end_date', 
        'end_time', 
        'has_party', 
        'description', 
        'created_by'
    ]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(ViewingParty)
admin.site.register(Photo)
