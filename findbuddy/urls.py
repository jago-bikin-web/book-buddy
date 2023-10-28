from django.urls import path, include
from findbuddy.views import *


app_name = 'findbuddy'


urlpatterns = [
    path('findbuddy/', show_findbuddy, name='findbuddy'),
    path('get-book/', get_book_json, name='get_book_json'),
]