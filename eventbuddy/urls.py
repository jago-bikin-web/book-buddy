from django.urls import path
from eventbuddy.views import *

app_name = 'eventbuddy'

urlpatterns = [
    path('', show_eventbuddy, name='show_eventbuddy'),
    path('create-event', create_event, name='create_event'),
]