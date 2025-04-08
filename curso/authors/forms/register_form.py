from django import forms
from django.contrib.auth.models import User

from utils.django_forms import add_placeholder, strong_password


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'your username')
        add_placeholder(self.fields['email'], 'your email')
        add_placeholder(self.fields['first_name'], 'your first name')
        add_placeholder(self.fields['last_name'], 'your last name')

    first_name = forms.CharField(
        label='First Name',
        required=True,
        error_messages={'required': 'Campo obrigatório.'},
    )

    email = forms.EmailField(
        label='Email',
        required=True,
        error_messages={'required': 'Campo obrigatório.'},
        help_text='the email must be valid'
    )

    password = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Your password'}),
        error_messages={'required': 'Campo obrigatório.'},
        help_text=(
            'Your password must contain at least 8 characters, '
            'including at least one uppercase letter, one lowercase letter and one number.'
        ),
        validators=[strong_password],
    )

    password2 = forms.CharField(
        label='Confirm Password',
        required=True,
        error_messages={'required': 'Campo obrigatório.'},
        widget=forms.PasswordInput(attrs={'placeholder': 'repeat your password'}),
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password',
            'email',
        ]
        # widgets = {
        #     'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
        # }
        # exclude = ['first_name']
        # labels = {'first_name': 'Nome',}
        # help_texts = {'email': 'the email must be valid'}
    
        error_messages = {
            'username': {'required': 'Campo obrigatório.'},
            } # invalid, required, disabled, readonly 
        # widgets = {'first_name': forms.TextInput(attrs={'class': 'form-control' attr1='value1', 'attr2': 'value2'})}

    # def clean_password(self):
    #     password = self.cleaned_data.get('password')
    #     if len(password) < 8:
    #         raise forms.ValidationError('Password must contain at least 8 characte rs')
    #     return password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists', code='invalid')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError({'password2': 'Passwords do not match'})
        return cleaned_data
