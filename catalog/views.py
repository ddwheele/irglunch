import datetime
import random
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.urls import reverse
from catalog.models import Person, HostAction, GuestAction
from django.contrib.auth.decorators import login_required
from catalog.forms import AddGuestForm, ChangeHostForm, AddPersonForm


HOST_COEFFICIENT = 1 # each time you host, it removes this many chances from your probability
IMMUNITY_PERIOD = 31 # after you host, you won't be asked to host again for this many days

# if the first of the month is the key (Monday=1, Sunday=7)
# then the value is the date of the first Tuesday
tues_translator = {1:2, 2:1, 3:7, 4:6, 5:5, 6:4, 7:3}

@login_required
def calculate_current_month_assignments(request):
    today = datetime.date.today()
    calculate_month_of_assignments(today)
    return HttpResponseRedirect('/')

@login_required
def calculate_next_month_assignments(request):
    today = datetime.date.today()
    day_next_month = get_next_month(today)
    calculate_month_of_assignments(day_next_month)
    return HttpResponseRedirect('next_month')

def calculate_month_of_assignments(a_day):
    """takes in a day, creates host assignments for each Tuesday in that month"""
    the_first = a_day.replace(day=1)
    weekday = the_first.isoweekday()
    first_tuesday = the_first.replace( day=tues_translator[weekday] )

    week = datetime.timedelta(days=7)

    for i in range(5):
        next_tues = first_tuesday + i*week
        if next_tues.month == first_tuesday.month:
            # make sure there isn't already a host assigned to that day
            host_action = HostAction.objects.filter(date=next_tues)
            if host_action.exists() and (host_action[0].host.name != 'unassigned'):
                continue
            else:
                assign_host(next_tues)
    return HttpResponseRedirect('/')

def assign_host(lunchdate):
    immune_date = lunchdate - datetime.timedelta(days=IMMUNITY_PERIOD)
    people = Person.objects.filter(active = True, last_hosted__lte=immune_date)
    denominator = 0 # total chances of anybody being picked to host
    for peep in people:
        denominator += peep.num_guest_actions - HOST_COEFFICIENT * peep.num_host_actions

    if denominator > 0: 
        selected = random.randint(0,denominator)
        chances = 0
        for peep in people:
            chances += peep.num_guest_actions - HOST_COEFFICIENT * peep.num_host_actions
            if selected <= chances:
                actions = HostAction.objects.filter(date=lunchdate)
                if actions.exists():
                    ha = actions[0]
                    ha.host = peep
                    # caveat: we aren't decrementing hosted counts because
                    # only 'unassigned' should ever be auto-reassigned
                else:
                    ha = HostAction(date=lunchdate, host=peep)
                ha.save()
                peep.num_host_actions = peep.num_host_actions + 1
                peep.last_hosted = lunchdate
                peep.save()
                return 
    else:
        # If we weren't able to assign anybody, give to "unassigned"
        unassigned_name = 'unassigned'
        nobodies = Person.objects.filter(name=unassigned_name)
        if nobodies.exists():
            nobody = nobody[0]
        else:
            nobody = Person(name=unassigned_name, active=False)
            nobody.save()
        ha = HostAction(date=lunchdate, host=nobody)
        ha.save()

@login_required
def single_lunch_listing(request, year, month, day):
    context = {}
    host_action = HostAction.objects.filter(date__year = year,
                                            date__month = month,
                                            date__day = day)
    if host_action.exists():
        context['host_action'] = host_action[0]
    else:
        context['host_action'] = 'unassigned'

    guest_actions = GuestAction.objects.filter(date__year = year,
                                               date__month = month,
                                               date__day = day).order_by('guest')

    context['guestaction_list'] = guest_actions    
    context['date'] = datetime.date(year=year, month=month, day=day)

    return render(request, 'catalog/single_lunch_listing.html', context=context)

@login_required
def index(request):
    context = {}
    today = datetime.date.today()
    host_action_list = HostAction.objects.filter(date__year = today.year,
                                            date__month = today.month).order_by('date')
    context['host_actions'] = host_action_list

    return render(request, 'index.html', context=context)

@login_required
def archive(request):
    context = {}
    today = datetime.date.today()
    host_action_list = HostAction.objects.filter(date__lte=today).order_by('-date')
    context['host_actions'] = host_action_list
    return render(request, 'archive.html', context=context)


@login_required
def next_month(request):
    context = {}
    today = datetime.date.today()
    day_next_month = get_next_month(today)
    host_action_list = HostAction.objects.filter(date__year = day_next_month.year,
                                                 date__month = day_next_month.month)
    context['host_actions'] = host_action_list

    return render(request, 'next_month.html', context=context)
  
@login_required
def add_person(request):
    if request.method == 'POST':
        form = AddPersonForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = AddPersonForm()

    context = {
        'form' : form,
    }
    return render(request, 'catalog/add_person.html', context)

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
        all_people = Person.objects.all()
        already_attending = Person.objects.select_related().filter(guestaction__date=lunchdate).distinct()
        form.fields['guest'].queryset = all_people.difference(already_attending)

    context = {
        'form' : form,
    }

    return render(request, 'catalog/add_guest.html', context)

@login_required
def change_host(request, pk):
    host_action = get_object_or_404(HostAction, pk=pk)

    shirking_host = host_action.host
    past_hosted = HostAction.objects.filter(host=shirking_host).order_by('-date')
    if past_hosted.exists() and past_hosted.count() > 1:
        last_hosted = past_hosted[1].date
    else:
        last_hosted = datetime.datetime(year=1900,month=5,day=23)

    if request.method == 'POST':
        form = ChangeHostForm(request.POST)

        if form.is_valid():
            new_host = form.cleaned_data['host']
            host_action.host = new_host
            host_action.save()
            new_host.num_host_actions = new_host.num_host_actions + 1
            new_host.last_hosted = host_action.date
            new_host.save()
            shirking_host.num_host_actions = shirking_host.num_host_actions-1
            shirking_host.last_hosted = last_hosted
            shirking_host.save()
            return HttpResponseRedirect(reverse('single-lunch-listing', kwargs={'year':host_action.date.year,
                                                                                'month':host_action.date.month,
                                                                                'day':host_action.date.day}))
    else:
        form = ChangeHostForm()

    context = {
        'form': form,
        'host_action': host_action
    }

    return render(request, 'catalog/change_host.html', context)

# used for debugging
def reset_hosted_dates(request):
    people = Person.objects.all()
    for peep in people:
        peep.last_hosted = datetime.datetime(year=2000, month=5, day =5)
        peep.save()
    context = {}
    context['peeps'] = people
    return render(request, 'catalog/debug.html', context=context)

def get_next_month(today):
    """given a date, return a date in the next month"""
    next_month = today.month + 1
    if next_month == 13:
        next_year = today.year + 1
        day_next_month = today.replace(month=1, year=next_year)
    else:
        day_next_month = today.replace(month=next_month)
    return day_next_month
 





















