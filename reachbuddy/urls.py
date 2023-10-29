from django.urls import path
from reachbuddy.views import *

app_name = 'reachbuddy'

urlpatterns = [
    path('', show_reachbuddy, name='show_reachbuddy'),
    path('create-thread', create_thread, name='create_thread'),
    path('json/', show_json, name='show_json'), 
    path('trash_thread/<int:id>', trash_thread, name='trash_thread'),
    path('get-books/', get_books_json, name='get_books_json'),
]