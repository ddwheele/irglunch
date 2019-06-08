import datetime
from django.shortcuts import render
from django.views.generic import ListView
from catalog.models import Person, HostAction, GuestAction

# if the first of the month is the key (Monday=1, Sunday=7)
# then the value is the date of the first Tuesday
tues_translator = {1:2, 2:1, 3:7, 4:6, 5:5, 6:4, 7:3}

def index(request):
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
 
class GuestList(ListView):
    model = GuestAction
    context_object_name = 'guestaction_list' 
    template_name = 'guestaction_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['host'] = HostAction.objects.all()
        return context






























    # Then you can click on each date and have it list the host, guests,
    # and a form to add yourself

