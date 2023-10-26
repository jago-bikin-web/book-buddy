from django.urls import path
from main.views import *
from eventbuddy.views import show_eventbuddy


app_name = 'main'


urlpatterns = [
    path('', show_landing_page, name='landing_page'),
    path('login/', login_user, name='login'),
    path('register/', register_user, name='register'),
]