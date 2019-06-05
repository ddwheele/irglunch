from django.db import models
from django.urls import reverse

# Create your models here.
class Person(models.Model):
    """Represents a person who hosts or eats IRG lunch"""
    name = models.CharField(max_length=50, help_text="Enter person's name or nickname")
    active = models.BooleanField(default=True, help_text='Is this person a possible IRG lunch host?')

    def __str__(self):
        return self.name

class TheHost(models.Model):
    """Represents one time a Person brings IRG lunch"""
    person = models.ForeignKey('Person', on_delete=models.SET_NULL, null=True, help_text="Person who brings IRG lunch")
    lunch_event = models.ForeignKey('LunchEvent', on_delete=models.SET_NULL, null=True, help_text="Instance of IRG Lunch")

    def __str__(self):
        return self.person.name + " brought IRG Lunch"

class AGuest(models.Model):
    """Represents one time a Person attends IRG lunch"""
    person = models.ForeignKey('Person', on_delete=models.SET_NULL, null=True, help_text="Person who attends IRG lunch")
    lunch_event = models.ForeignKey('LunchEvent', on_delete=models.SET_NULL, null=True, help_text="Instance of IRG Lunch")
    note = models.CharField(max_length=200, help_text="Note to host, ie, vegetarian")

    def __str__(self):
        return self.person.name + " attended IRG Lunch"

class LunchEvent(models.Model):
    """Represents the IRG Lunch that happened on a particular date"""
    date = models.DateField(null=True, blank=True, help_text="Date of this IRG Lunch")
    host = models.ForeignKey('TheHost', on_delete=models.SET_NULL, null=True, help_text="Person who brings IRG lunch")
    guest = models.ForeignKey('AGuest', on_delete=models.SET_NULL, null=True, help_text="People who attend IRG lunch")

    def __str__(self):
        return self.date

    def get_absolute_url(self):
        """Returns the url to access a detail record for this lunch"""
        return reverse('lunch-detail', args=[str(self.id)])




