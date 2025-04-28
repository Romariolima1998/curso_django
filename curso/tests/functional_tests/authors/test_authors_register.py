import time
import pytest

from .base import AuthorsBaseTest

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


@pytest.mark.functional_test
class authorsRegisterTest(AuthorsBaseTest):
    
    def fill_form_dummy_data(self, form):

        fields = form.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():
                field.send_keys(" " * 20)

    def get_form(self):
        return self.browser.find_element(By.XPATH, '/html/body/main/div[2]/form[1]')       

    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + "/authors/register/")

        form = self.get_form()

        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('email@email.com')
        callback(form)
        return form

    def test_empty_first_name_error_message(self):
        def callback(form):
            first_name_field = self.get_by_placeholder(form, "your first name")
            first_name_field.send_keys(" ")

            first_name_field.send_keys(Keys.ENTER)

            form = self.get_form()
            self.assertIn('Campo obrigatório.', form.text)

        self.form_field_test_with_callback(callback)

    def test_empty_last_name_error_message(self):
        def callback(form):
            last_name_field = self.get_by_placeholder(form, "your last name")
            last_name_field.send_keys(" ")

            last_name_field.send_keys(Keys.ENTER)

            

            form = self.get_form()
            self.assertIn('Campo obrigatório.', form.text)

        self.form_field_test_with_callback(callback)

    def test_empty_username_error_message(self):
        def callback(form):
            username_field = self.get_by_placeholder(form, "your username")
            username_field.send_keys(" ")

            username_field.send_keys(Keys.ENTER)
            
            form = self.get_form()
            self.assertIn('Campo obrigatório.', form.text)

        self.form_field_test_with_callback(callback)

    def test_invalid_email_error_message(self):
        def callback(form):
            email_field = self.get_by_placeholder(form, "your email")
            email_field.send_keys("email@email")

            email_field.send_keys(Keys.ENTER)
            
            form = self.get_form()
            self.assertIn('the email must be valid', form.text)

        self.form_field_test_with_callback(callback)

    def test_empty_password_error_message(self):
        def callback(form):
            password = self.get_by_placeholder(form, "Your password")
            password2 = self.get_by_placeholder(form, "repeat your password")
            password.send_keys("Abc@1234")
            password2.send_keys("Abc@1234diferente")

            password2.send_keys(Keys.ENTER)
            
            form = self.get_form()
            self.assertIn('Passwords do not match', form.text)

        self.form_field_test_with_callback(callback)

    def test_user_valid_data_register_succesfully(self):
        self.browser.get(self.live_server_url + "/authors/register/")

        form = self.get_form()

        self.get_by_placeholder(form, "your first name").send_keys("Lucas")
        self.get_by_placeholder(form, "your last name").send_keys("Lima")
        self.get_by_placeholder(form, "your username").send_keys("lucas")
        self.get_by_placeholder(form, "your email").send_keys("email@email.com")
        self.get_by_placeholder(form, "Your password").send_keys("Abc@1234")
        self.get_by_placeholder(form, "repeat your password").send_keys("Abc@1234")

        form.submit()
        time.sleep(1)
        self.assertIn('User created successfully', self.browser.find_element(By.TAG_NAME, 'body').text)


        

