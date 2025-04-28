import pytest
import time

from .base import AuthorsBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.functional_test
class authorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        strng_password = 'testpassword'
        user = User.objects.create_user(
            username='testuser',
            password=strng_password,
            first_name='Test',
            last_name='User',
        )
        user.save()
        self.browser.get(self.live_server_url + reverse('authors:login'))

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_input = form.find_element(By.XPATH, '//input[@placeholder="your username"]')
        password_input = form.find_element(By.XPATH, '//input[@placeholder="your password"]')
        username_input.send_keys(user.username)
        password_input.send_keys(strng_password)
        password_input.send_keys(Keys.RETURN)
        time.sleep(1)

        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn(f'you are logged in with {user.username}', body.text)

    def test_login_created_raiases_404_if_not_POST(self):
        self.browser.get(self.live_server_url + reverse('authors:login_create'))

        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
            )

    def test_form_login_is_invalid(self):
        self.browser.get(self.live_server_url + reverse('authors:login'))

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_input = form.find_element(By.XPATH, '//input[@placeholder="your username"]')
        password_input = form.find_element(By.XPATH, '//input[@placeholder="your password"]')
        username_input.send_keys(' ')
        password_input.send_keys(' ')
        password_input.send_keys(Keys.RETURN)
        time.sleep(1)

        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Invalid username or password', body.text)

    def test_form_login_is_invalid_credentials(self):
        self.browser.get(self.live_server_url + reverse('authors:login'))

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_input = form.find_element(By.XPATH, '//input[@placeholder="your username"]')
        password_input = form.find_element(By.XPATH, '//input[@placeholder="your password"]')
        username_input.send_keys('usuario_invalido')
        password_input.send_keys('senha_invalida')
        password_input.send_keys(Keys.RETURN)
        time.sleep(1)

        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Invalid credentials', body.text)