from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:year>/<int:month>/<int:day>', views.single_lunch_listing, name = 'single-lunch-listing'),
    path('<int:year>/<int:month>/<int:day>/add_guest', views.add_guest, name='add-guest'),
    path('<uuid:pk>/change_host', views.change_host, name='change-host'),
    path('calculate_month_of_assignments', views.calculate_month_of_assignments),    
    path('reset_hosted_dates', views.reset_hosted_dates)
]
    
