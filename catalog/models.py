from django.db import models
from django.urls import reverse

# Create your models here.
class Person(models.Model):
    """Represents a person who hosts or eats IRG lunch"""
    name = models.CharField(max_length=50, help_text="Enter person's name or nickname")
    active = models.BooleanField(default=True, help_text='Is this person a possible IRG lunch host?')

    def __str__(self):
        return self.name

class HostAction(models.Model):
    """Represents one time a Person brings IRG lunch"""
    host = models.ForeignKey('Person', on_delete=models.SET_NULL, null=True, help_text="Person who brings IRG lunch")
    date = models.DateField(null=True, blank=True, help_text="Date of the IRG Lunch hosted")

    def __str__(self):
        return self.host.name + " brought IRG Lunch on " + str(self.date)

    def get_absolute_url(self):
        return reverse('lunch-view', kwargs={'year':self.date.year,'month':self.date.month, 'day':self.date.day})

class GuestAction(models.Model):
    """Represents one time a Person attends IRG lunch"""
    guest = models.ForeignKey('Person', on_delete=models.SET_NULL, null=True, help_text="Person who attends IRG lunch")
    date = models.DateField(null=True, blank=True, help_text="Date of the IRG Lunch attended")
    note = models.CharField(max_length=500, blank=True, help_text="Note to host, ie, vegetarian")

    def __str__(self):
        return self.guest.name + " attended IRG Lunch on " + str(self.date)


