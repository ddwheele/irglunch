from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('archive', views.archive, name='archive'),
    path('next_month', views.next_month, name='next-month'),
    path('<int:year>/<int:month>/<int:day>', views.single_lunch_listing, name = 'single-lunch-listing'),
    path('<int:year>/<int:month>/<int:day>/add_guest', views.add_guest, name='add-guest'),
    path('<uuid:pk>/change_host', views.change_host, name='change-host'),
    path('add_person', views.add_person, name='add-person'),
    path('calculate_current_month_assignments', views.calculate_current_month_assignments),    
    path('calculate_next_month_assignments', views.calculate_next_month_assignments),    
    path('reset_hosts', views.reset_hosts)
]
    
