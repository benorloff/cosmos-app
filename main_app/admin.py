from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Event, Profile, Photo, ViewingParty


from import_export.admin import ImportExportMixin
from .models import Task


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


class TaskAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['name', 'description', 'due_date', 'is_complete']


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Event)
admin.site.register(ViewingParty)
admin.site.register(Photo)
