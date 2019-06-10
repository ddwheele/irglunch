import datetime
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

def oldindex(request):
    """"View function for home page"""
    today = datetime.date.today()
    the_first = today.replace(day=1)
    weekday = the_first.isoweekday()
    month_name = today.strftime("%B")

    week = datetime.timedelta(days=7)
    tues0 = the_first.replace( day=tues_translator[weekday] )

    context = {
        'month_name' : today.strftime("%B"),
        'year' : today.year,
    } 

    for i in range(5):
        next_tues = tues0 + i*week
        if next_tues.month == tues0.month:
            context['week'+str(i)] = next_tues
            next_host = HostAction.objects.filter(date__year = next_tues.year,
						  date__month = next_tues.month,
						  date__day = next_tues.day)
            if next_host.exists():
                context['host'+str(i)] = next_host[0].host.name
            else:
                context['host'+str(i)] = 'unassigned'
    
    return render(request, 'index.html', context=context)

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
            return HttpResponseRedirect(reverse('lunch-view', kwargs={'year':year,'month':month,'day':day}))
    else:
        lunchdate = datetime.date(year, month, day)
        form = AddGuestForm(initial={'date': lunchdate})

    context = {
        'form' : form
    }

    return render(request, 'catalog/add_guest.html', context)


























