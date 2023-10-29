from django.urls import path
from reachbuddy.views import *

app_name = 'reachbuddy'

urlpatterns = [
    path('', show_reachbuddy, name='show_reachbuddy'),
    path('create-thread', create_thread, name='create_thread'),
    path('json/', show_json, name='show_json'), 
    path('json_book/', show_json_book, name='show_json_book'), 
    path('json_user/', show_json_user, name='show_json_user'), 
    path('json_user_id/<int:id>/', show_json_user_id, name='show_json_user_id'),
    path('trash_thread/<int:id>', trash_thread, name='trash_thread'),
    path('get-books/', get_books_json, name='get_books_json'),
    path('get-threads/', get_threads_json, name='get_threads_json'),
    path('get_book_json_id/<int:id>/', get_book_json_id, name='get_book_json_id'),
    path('get_profile_json_id/<int:id>/', get_profile_json_id, name='get_profile_json_id'),
    path('create_thread_ajax/<int:id>/', create_thread_ajax, name='create_thread_ajax'),
    path('delete_thread_ajax/<int:id>/', delete_thread_ajax, name='delete_thread_ajax'),
]