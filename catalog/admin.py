from django.contrib import admin
from catalog.models import Person, HostAction, GuestAction


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name','active', 'num_guest_actions','num_host_actions','last_hosted')
    list_filter = ('active','num_host_actions','num_guest_actions')


@admin.register(HostAction)
class HostActionAdmin(admin.ModelAdmin):
    list_display = ('host', 'date')
    list_filter = ('host', 'date')

@admin.register(GuestAction)
class GuestActionAdmin(admin.ModelAdmin):
    list_display = ('guest', 'date')
    list_filter = ('guest', 'date')

