from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class SignupTests(TestCase):
    def test_signup_page(self):
        response = self.client.get(reverse('common:signup'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'common/signup.html')

    def test_signup_creates_user(self):
        response = self.client.post(
            reverse('common:signup'),
            {
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password1': 'strong-test-pass1234',
                'password2': 'strong-test-pass1234',
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_page(self):
        response = self.client.get(reverse('common:login'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'common/login.html')