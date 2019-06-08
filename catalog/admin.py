from django.contrib import admin
from catalog.models import Person, HostAction, GuestAction


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_filter = ('active','name')


@admin.register(HostAction)
class HostActionAdmin(admin.ModelAdmin):
    list_display = ('host', 'date')
    list_filter = ('host', 'date')

@admin.register(GuestAction)
class GuestActionAdmin(admin.ModelAdmin):
    list_display = ('guest', 'date')
    list_filter = ('guest', 'date')

