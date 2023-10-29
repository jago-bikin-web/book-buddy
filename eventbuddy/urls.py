from django.urls import path
from eventbuddy.views import *

app_name = 'eventbuddy'

urlpatterns = [
    path('', show_eventbuddy, name='show_eventbuddy'),
    path('create-event', create_event, name='create_event'),
    path('edit-event/<int:id>', edit_event, name='edit_event'),
    path('delete/<int:id>', delete_event, name='delete_event'),
    path('regis-event/<int:id>', regis_event, name='regis_event'),
    path('attendees/<int:id>', show_attendees, name='show_attendees'),
    path('get-event/', get_event_json, name='get_event_json'),
    path('create-event-ajax/', add_event_ajax, name='add_event_ajax'),
    path('get-books-ID/<int:id>', get_book_json, name='get_book_json'),
]
