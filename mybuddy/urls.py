from django.urls import path
from mybuddy.views import *


app_name = 'mybuddy'


urlpatterns = [
    path('', show_my_buddy, name='my_buddy'),
    path('add-buddy/', add_buddy, name='add_buddy'),
    path('get-own-book/', get_owned_book, name='get_owned_book'),
    path('update-own-book/', update_own_book, name='update_own_book'),
    path('add-page-track/', add_page_track, name='add_page_track'),
    path('sub-page-track/', sub_page_track, name='sub_page_track'),
    path('update-book-flutter/', update_book_flutter, name='update_book_flutter'),
    path('add-book-flutter/', add_book_flutter, name='add_book_flutter'),
]