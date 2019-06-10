from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:year>/<int:month>/<int:day>', views.lunch_list_view, name = 'lunch-view'),
    path('<int:year>/<int:month>/<int:day>/addguest', views.add_guest, name='add-guest')
]
