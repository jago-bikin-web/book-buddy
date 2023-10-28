from django.urls import path
from mybuddy.views import *


app_name = 'mybuddy'


urlpatterns = [
    path('', show_my_buddy, name='my_buddy'),
    path('add-buddy/', add_buddy, name='add_buddy'),
    path('get-own-book/', get_owned_book, name='get_owned_book')
]