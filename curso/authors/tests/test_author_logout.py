from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class AuthorLogoutTest(TestCase):
    def test_author_logout_using_get_method(self):
        user = User.objects.create_user(
            username='testuser', password='testpassword'
            )
        user.save()
        self.client.login(username='testuser', password='testpassword')
        # Test the author logout functionality
        response = self.client.get(reverse('authors:logout'), follow=True)
        self.assertEqual(response.status_code, 404)

    def test_user_try_logout_another_user(self):
        user = User.objects.create_user(
            username='testuser', password='testpassword'
            )
        user.save()
        self.client.login(username='testuser', password='testpassword')
        # Test the author logout functionality
        response = self.client.post(
            reverse('authors:logout'),
            data={'username': 'anotheruser'},
            follow=True)
        self.assertIn('Invalid credentials', response.content.decode())

    def test_user_logout_successfully(self):
        user = User.objects.create_user(
            username='testuser', password='testpassword'
            )
        user.save()
        self.client.login(username='testuser', password='testpassword')
        # Test the author logout functionality
        response = self.client.post(
            reverse('authors:logout'),
            data={'username': user.username},
            follow=True)
        self.assertIn('Logout successfully', response.content.decode())
