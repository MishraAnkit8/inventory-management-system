# inventory/tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_login_success(self):
        response = self.client.post(reverse('login_view'), {
            'loginDetails': {
                'userEmail': 'testuser',
                'userPassword': 'testpass'
            }
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
