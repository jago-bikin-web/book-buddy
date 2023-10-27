from django.urls import path
from book.views import *

app_name = 'book'

urlpatterns = [
    path('fetch-data/', add_book_from_google_books_api, name='fetch_data'),
    path('get-books/', get_books, name='get_book'),
    path('get-random/', get_random_books, name='get_random_books'),
]