from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'your username',
            'class': 'form-control'
        }),
        error_messages={
            'required': 'Campo obrigatório.'
        }
    )
    password = forms.CharField(
        label='Password',
        max_length=128,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'your password',
            'class': 'form-control'
        }),
        error_messages={
            'required': 'Campo obrigatório.'
        }
    )