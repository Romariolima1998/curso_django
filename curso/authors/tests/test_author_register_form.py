from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from authors.forms import RegisterForm
from django.urls import reverse

from parameterized import parameterized


class AuthorRegisterFormTest(TestCase):
    @parameterized.expand([
        ('username', 'your username'),
        ('email', 'your email'),
        ('first_name', 'your first name'),
        ('last_name', 'your last name'),
        ('password', 'Your password'),
        ('password2', 'repeat your password'),
    ])
    def test_fields_placeholder_is_correct(self, field_name, expected_placeholder):
        form = RegisterForm()
        placeholder = form.fields[field_name].widget.attrs['placeholder']
        self.assertEqual(placeholder, expected_placeholder)

    @parameterized.expand([
        ('password', ('Your password must contain at least 8 characters, '
         'including at least one uppercase letter, one lowercase letter and one number.')),
        ('email', 'the email must be valid')
    ])
    def test_fields_help_text(self, field_name, expected_help_text):
        form = RegisterForm()
        current = form.fields[field_name].help_text
        self.assertEqual(current, expected_help_text)

    @parameterized.expand([
        ('password', 'Password'),
        ('password2', 'Confirm Password'),
    ])
    def test_fields_label_text(self, field_name, expected_label):
        form = RegisterForm()
        current = form.fields[field_name].label
        self.assertEqual(current, expected_label)


class AuthorRegisterFormDjangoTest(DjangoTestCase):
    def setUp(self):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@email.com',
            'password': 'Password1',
            'password2': 'Password1',
        }
        return super().setUp()
    
    @parameterized.expand([
        ('username', 'Campo obrigatório.'),
        ('first_name', 'Campo obrigatório.'),
        ('email', 'Campo obrigatório.'),
        ('password', 'Campo obrigatório.'),
        ('password2', 'Campo obrigatório.'),
        
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''

        url = reverse('authors:register_create')
        response = self.client.post(url, {}, follow=True)
        self.assertIn(msg, response.context['form'].errors.get(field, []))
        # self.assertIn(msg, response.content.decode('utf-8'))

    def test_password_field_have_lower_upper_case_and_number(self):
        self.form_data['password'] = 'password'
        url = reverse('authors:register_create')
        response = self.client.post(url, self.form_data, follow=True)

        msg = ('Your password must contain at least 8 characters, '
             'including at least one uppercase letter, one lowercase letter and one number.')
        self.assertIn(msg, response.context['form'].errors.get('password', []))

    def test_password_and_password2_must_match(self):
        self.form_data['password2'] = 'password2'
        url = reverse('authors:register_create')
        response = self.client.post(url, self.form_data, follow=True)

        msg = 'Passwords do not match'
        self.assertIn(msg, response.context['form'].errors.get('password2', []))

    def test_send_get_request_to_registration_create_view_returns_404(self):
        url = reverse('authors:register_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_email_field_must_be_unique(self):
        self.form_data['email'] = 'email@email.com'

        url = reverse('authors:register_create')
        self.client.post(url, self.form_data, follow=True)
        response = self.client.post(url, self.form_data, follow=True)

        msg = 'Email already exists'

        self.assertIn(msg, response.context['form'].errors.get('email', []))

    def test_author_create_can_login(self):
        url = reverse('authors:register_create')
        self.client.post(url, self.form_data, follow=True)

        is_authenticated = self.client.login(
            username=self.form_data['username'],
            password=self.form_data['password'],
        )

        self.assertTrue(is_authenticated)