import re

from django import forms
from django.contrib.auth.models import User


def add_attr(field, attr_name, attr_new_val):
    existing_attrs = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attrs} {attr_new_val}'.strip()


def add_placeholder(field, placeholder):
    field.widget.attrs['placeholder'] = placeholder


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise forms.ValidationError(
            ('Your password must contain at least 8 characters, '
             'including at least one uppercase letter, one lowercase letter and one number.'),
            code='invalid'
        )


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'your username')
        add_placeholder(self.fields['email'], 'your email')
        add_placeholder(self.fields['first_name'], 'your first name')
        add_placeholder(self.fields['last_name'], 'your last name')

    password = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Your password'}),
        error_messages={'required': 'Password is required'},
        help_text=(
            'Your password must contain at least 8 characters, '
            'including at least one uppercase letter, one lowercase letter and one number.'
        ),
        validators=[strong_password],
    )

    password2 = forms.CharField(
        label='Confirm Password',
        required=True,
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
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
        }
        # exclude = ['first_name']
        # labels = {'first_name': 'Nome',}
        # help_texts = {'first_name': 'apenas primeiro nome',}
        # error_messages = {'first_name': {'required': 'Campo obrigatório',}} invalid, required, disabled, readonly 
        # widgets = {'first_name': forms.TextInput(attrs={'class': 'form-control' attr1='value1', 'attr2': 'value2'})}

    # def clean_password(self):
    #     password = self.cleaned_data.get('password')
    #     if len(password) < 8:
    #         raise forms.ValidationError('Password must contain at least 8 characte rs')
    #     return password
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError({'password2': 'Passwords do not match'})
        return cleaned_data
