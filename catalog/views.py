import datetime
import random
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse
from catalog.models import Person, HostAction, GuestAction
from django.contrib.auth.decorators import login_required
from catalog.forms import AddGuestForm


# if the first of the month is the key (Monday=1, Sunday=7)
# then the value is the date of the first Tuesday
tues_translator = {1:2, 2:1, 3:7, 4:6, 5:5, 6:4, 7:3}
host_coefficient = 2 # each time you host, it removes this many chances from your probability

@login_required
def calculate_lunch_month(request):
    """"View function for home page"""
    today = datetime.date.today()
    the_first = today.replace(day=1)
    weekday = the_first.isoweekday()

    week = datetime.timedelta(days=7)

    people = Person.objects.filter(active = True)
    denominator = 0 # total chances of anybody being picked to host
    for peep in people:
        denominator += peep.num_guest_actions - host_coefficient * peep.num_host_actions

 
    first_tuesday = the_first.replace( day=tues_translator[weekday] )

    ha1 = HostAction(date = first_tuesday)
 
    selected = random.randint(0,denominator)
    chances = 0
    for peep in people:
        chances = peep.num_guest_actions - host_coefficient * peep.num_host_actions
        if selected <= chances:    
            ha1.host = peep
            peep.num_host_actions = peep.num_host_actions + 1
            ha1.save()
            peep.save()
            break


#    for i in range(5):
#        next_tues = first_tuesday + i*week
#        if next_tues.month == first_tuesday.month:
#            context['week'+str(i)] = next_tues
#            next_host = HostAction.objects.filter(date__year = next_tues.year,
#						  date__month = next_tues.month,
#						  date__day = next_tues.day)
#            if next_host.exists():
#                context['host'+str(i)] = next_host[0].host.name
#            else#:
#                context['host'+str(i)] = 'unassigned'
    
    return HttpResponseRedirect('/')


@login_required
def lunch_list_view(request, year, month, day):
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

    return render(request, 'catalog/guestaction_list.html', context=context)

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
            return HttpResponseRedirect(reverse('lunch-view', kwargs={'year':year,'month':month,'day':day}))
    else:
        lunchdate = datetime.date(year, month, day)
        form = AddGuestForm(initial={'date': lunchdate})

    context = {
        'form' : form
    }

    return render(request, 'catalog/add_guest.html', context)


























