from django.shortcuts import render
from catalog.models import Person, HostAction, GuestAction
import datetime

# if the first of the month is the key (Monday=1, Sunday=7)
# then the value is the date of the first Tuesday
tues_translator = {1:2, 2:1, 3:7, 4:6, 5:5, 6:4, 7:3}

# Create your views here.
def index(request):
    """"View function for home page"""
    today = datetime.date.today()
    the_first = today.replace(day=1)
    weekday = the_first.isoweekday()
    month_name = today.strftime("%B")

    tues = []
    week = datetime.timedelta(days=7)
    tues.append( the_first.replace( day=tues_translator[weekday] ))
    for i in range(1,5):
        tues.append(tues[0] + (i*week))

    context = {
        'month_name' : today.strftime("%B"),
        'year' : today.year,
        'month' : today.month,
        'week1' : tues[0].day,
        'week2' : tues[1].day,
        'week3' : tues[2].day,
        'week4' : tues[3].day,
        'host1' : 'alex',
        'host2' : 'betty',
        'host3' : 'cory',
        'host4' : 'danielle'
        
    } 

    if tues[4].month == tues[0].month:
        context['week5'] = tues[5].day

    
    return render(request, 'index.html', context=context)


    # Then you can click on each date and have it list the host, guests,
    # and a form to add yourself

