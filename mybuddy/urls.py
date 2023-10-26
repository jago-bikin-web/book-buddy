from django.urls import path
from mybuddy.views import *


app_name = 'mybuddy'


urlpatterns = [
    path('', show_my_buddy, name='my_buddy'),
]