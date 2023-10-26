from django.urls import path
from eventbuddy.views import show_eventbuddy

app_name = 'eventbuddy'

urlpatterns = [
    path('', show_eventbuddy, name='show_eventbuddy'),
]