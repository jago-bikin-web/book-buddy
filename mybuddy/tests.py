# from django.test import TestCase
import json

from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from mybuddy.views import *
from mybuddy.models import OwnedBook
from main.models import Profile

# Create your tests here.
class AppTest(TestCase):
    # ----------------- Test Authenticated ----------------- #
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        Profile.objects.create(user=self.user)
    
    def test_authenticated_user_can_access_view_1(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('mybuddy:my_buddy'))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_can_access_view_2(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('mybuddy:add_buddy'))
        self.assertEqual(response.status_code, 200)
    
    def test_unauthenticated_user_cannot_access_view_1(self):
        response = self.client.get(reverse('mybuddy:my_buddy'))
        self.assertEqual(response.status_code, 302)

    def test_unauthenticated_user_cannot_access_view_2(self):
        response = self.client.get(reverse('mybuddy:add_buddy'))
        self.assertEqual(response.status_code, 302)

    # --------------------- URL ---------------------------- #
    def test_show_my_buddy_url(self):
        url = reverse("mybuddy:my_buddy")
        self.assertEqual(resolve(url).func, show_my_buddy)
    def test_add_buddy_url(self):
        url = reverse("mybuddy:add_buddy")
        self.assertEqual(resolve(url).func, add_buddy)
    def test_get_own_book_url(self):
        url = reverse("mybuddy:get_owned_book")
        self.assertEqual(resolve(url).func, get_owned_book)
    def test_update_own_book_url(self):
        url = reverse("mybuddy:update_own_book")
        self.assertEqual(resolve(url).func, update_own_book) 
    def test_add_page_track_url(self):
        url = reverse("mybuddy:add_page_track")
        self.assertEqual(resolve(url).func, add_page_track)
    def test_sub_page_track_url(self):
        url = reverse("mybuddy:sub_page_track")
        self.assertEqual(resolve(url).func, sub_page_track)

    # --------------------- Views ---------------------------- #
    def test_view_show_mybuddy(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('mybuddy:my_buddy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mybuddy.html")

    def test_view_show_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('mybuddy:add_buddy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "addbuddy.html")
