import uuid
from django.db import models
from django.urls import reverse
import datetime as dt

# Create your models here.
class Person(models.Model):
    """Represents a person who hosts or eats IRG lunch"""
    name = models.CharField(max_length=50, help_text="Enter person's name or nickname")
    active = models.BooleanField(default=True, help_text='Is this person a possible IRG lunch host?')
    num_guest_actions = models.IntegerField(default=1, help_text='Times person has attended IRG lunch')
    num_host_actions = models.IntegerField(default=0, help_text='Times person has hosted IRG lunch')
    last_hosted = models.DateField(default=dt.datetime(year=dt.MINYEAR,month=1,day=1),
                                   help_text='Date of last time person hosted IRG lunch')

    def __str__(self):
        return self.name

class HostAction(models.Model):
    """Represents one time a Person brings IRG lunch"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,help_text='Unique ID for this hosting action')
    host = models.ForeignKey('Person', on_delete=models.SET_NULL, null=True, help_text="Person who brings IRG lunch")
    date = models.DateField(null=True, blank=True, help_text="Date of the IRG Lunch hosted")
    comment = models.TextField(blank=True, help_text="Information about this IRG Lunch, ie, restaurant")

    def __str__(self):
        hostname = "-"
        if self.host is not None:
            hostname = self.host.name
        return hostname + " brought IRG Lunch on " + str(self.date)

    def get_absolute_url(self):
        return reverse('single-lunch-listing', kwargs={'year':self.date.year,'month':self.date.month, 'day':self.date.day})

class GuestAction(models.Model):
    """Represents one time a Person attends IRG lunch"""
    guest = models.ForeignKey('Person', on_delete=models.SET_NULL, null=True, help_text="Person who attends IRG lunch")
    date = models.DateField(null=True, blank=True, help_text="Date of the IRG Lunch attended")
    note = models.CharField(max_length=500, blank=True, help_text="Note to host, ie, vegetarian")

    def __str__(self):
        guestname = "-"
        if self.guest is not None:
            guestname = guest.host.name
        return guestname + " attended IRG Lunch on " + str(self.date)


