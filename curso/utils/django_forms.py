from django import forms
import re


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
