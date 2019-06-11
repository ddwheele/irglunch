import datetime
import random
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse
from catalog.models import Person, HostAction, GuestAction
from django.contrib.auth.decorators import login_required
from catalog.forms import AddGuestForm


HOST_COEFFICIENT = 1 # each time you host, it removes this many chances from your probability
IMMUNITY_PERIOD = 31 # after you host, you won't be asked to host again for this many days

# if the first of the month is the key (Monday=1, Sunday=7)
# then the value is the date of the first Tuesday
tues_translator = {1:2, 2:1, 3:7, 4:6, 5:5, 6:4, 7:3}

def assign_host(lunchdate):
    immune_date = lunchdate - datetime.timedelta(days=IMMUNITY_PERIOD)
    people = Person.objects.filter(active = True, last_hosted__lte=immune_date)
    denominator = 0 # total chances of anybody being picked to host
    for peep in people:
        denominator += peep.num_guest_actions - HOST_COEFFICIENT * peep.num_host_actions
 
    selected = random.randint(0,denominator)
    chances = 0
    for peep in people:
        chances += peep.num_guest_actions - HOST_COEFFICIENT * peep.num_host_actions
        if selected <= chances:    
            ha = HostAction(date=lunchdate)
            ha.host=peep
            ha.save()
            peep.num_host_actions = peep.num_host_actions + 1
            peep.last_hosted = lunchdate
            peep.save()
            return 

    #return people

def reset_hosted_dates(request):
    people = Person.objects.all()
    for peep in people:
        peep.last_hosted = datetime.datetime(year=2000, month=5, day =5)
        peep.save()
    context = {}
    context['peeps'] = people
    return render(request, 'catalog/debug.html', context=context)

#    return HttpResponseRedirect('/')

@login_required
def calculate_month_of_assignments(request):
    """"View function for home page"""
    today = datetime.date.today()
    the_first = today.replace(day=1)
    weekday = the_first.isoweekday()
    first_tuesday = the_first.replace( day=tues_translator[weekday] )

    week = datetime.timedelta(days=7)

    for i in range(5):
        next_tues = first_tuesday + i*week
        if next_tues.month == first_tuesday.month:
            assign_host(next_tues)
    return HttpResponseRedirect('/')


@login_required
def single_lunch_listing(request, year, month, day):
    context = {}
    host_action = HostAction.objects.filter(date__year = year,
                                            date__month = month,
                                            date__day = day)
    if host_action.exists():
        context['host'] = host_action[0].host.name
    else:
        context['host'] = 'unassigned'

    guest_actions = GuestAction.objects.filter(date__year = year,
                                               date__month = month,
                                               date__day = day).order_by('guest')

    context['guestaction_list'] = guest_actions    
    context['year'] = year
    context['month'] = month
    context['day'] = day

    return render(request, 'catalog/single_lunch_listing.html', context=context)

@login_required
def index(request):
    context = {}
    today = datetime.date.today()
    host_action_list = HostAction.objects.filter(date__year = today.year,
                                            date__month = today.month).order_by('date')
    context['host'] = host_action_list

    return render(request, 'index.html', context=context)

@login_required
def add_guest(request, year, month, day):
    if request.method == 'POST':
        
        form = AddGuestForm(request.POST)
        
        if form.is_valid():
            form.save()
            guest = form.cleaned_data['guest']
            guest.num_guest_actions = guest.num_guest_actions + 1
            guest.save()
            return HttpResponseRedirect(reverse('single-lunch-listing', kwargs={'year':year,'month':month,'day':day}))
    else:
        lunchdate = datetime.date(year, month, day)
        form = AddGuestForm(initial={'date': lunchdate})

    context = {
        'form' : form
    }

    return render(request, 'catalog/add_guest.html', context)


























