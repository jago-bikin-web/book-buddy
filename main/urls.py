from django.urls import path
from main.views import *


app_name = 'main'


urlpatterns = [
    path('', show_landing_page, name='landing_page'),
    path('home/', home, name='home'),
    path('login/', login_user, name='login'),
    path('register/', register_user, name='register'),
    path('logout/', logout_user, name='logout'),
]