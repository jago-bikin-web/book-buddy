from django.test import TestCase
from django.urls import reverse

# Create your tests here.

class AppTest(TestCase):
    # ----------------- Test Authenticated ----------------- #
    def test_aman(self):
        response = self.client.post(path=reverse("authentication:register"), data={
            "full_name": "test",
            "username": "test",
            "email": "test",
            "status": "M",
            "password1": "test",
            "password2": "test"
        }, content_type="application/json")

        self.assertEqual(response.json(), {
            "username": "test",
            "fullName": "test",
            "userId": 1,
            "email": "test",
            "role": "M",
            "status": True,
            "message": "Register dan login berhasil!"
        })
