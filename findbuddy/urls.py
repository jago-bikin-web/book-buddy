from django.urls import path, include
from findbuddy.views import *


app_name = 'findbuddy'

urlpatterns = [
    path('', show_findbuddy, name='findbuddy'),
    path('get-book/', get_book_json, name='get_book_json'),
    path('get-request/', get_request_json, name='get_request_json'),
    path('add-request-ajax/', add_request_ajax, name='add_request_ajax'),
    path('json/', show_json, name='show_json'), 
    path('get-search-books/', get_search_books, name='search_books'), 
    path('create-flutter/', create_request_flutter, name='create_request_flutter'),
]

