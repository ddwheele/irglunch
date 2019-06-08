from django.urls import path
from catalog.views import GuestList
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<year>-<month>-<day>', GuestList.as_view()),
]
