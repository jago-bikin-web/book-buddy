from django.urls import path
from reachbuddy.views import *

app_name = 'main'

urlpatterns = [
    path('', show_reachbuddy, name='show_reachbuddy'),
]