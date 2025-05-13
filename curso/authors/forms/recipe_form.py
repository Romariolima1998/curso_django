from collections import defaultdict
from django.core.exceptions import ValidationError

from django import forms
from recipes.models import Recipe

from utils.django_forms import add_attr


def is_positive_number(value):
    try:
        number = float(value)
    except ValueError:
        return False
    return number > 0


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_attr(self.fields['preparation_steps'], 'class', 'span-2')
        self._my_errors = defaultdict(list)

    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'preparation_time',
            'preparation_time_unit',
            'servings',
            'servings_unit',
            'preparation_steps',
            'cover',
        ]
        widgets = {
            'cover': forms.FileInput(attrs={
                'class': 'span-2',
            }),
            'servings_unit': forms.Select(
                choices=(
                    ('porcoes', 'Porções'),
                    ('fatias', 'Fatias'),
                    ('pessoas', 'Pessoas'),
                )),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('minutos', 'minutos'),
                    ('horas', 'horas'),
                    ('dias', 'dias'),
                )),
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        cd = self.cleaned_data
        title = cd.get('title', '')
        description = cd.get('description', '')

        if len(title) < 5:
            self._my_errors['title'].append(
                'Title must be at least 5 characters long'
            )
        if len(description) < 5:
            self._my_errors['description'].append(
                'Description must be at least 5 characters long'
            )

        if self._my_errors:
            raise ValidationError(self._my_errors)
        return super_clean

    def clean_preparation_time(self):
        preparation_time = self.cleaned_data.get('preparation_time')
        if not is_positive_number(preparation_time):
            self._my_errors['preparation_time'].append(
                'Preparation time must be a positive number'
            )
        return preparation_time

    def clean_servings(self):
        servings = self.cleaned_data.get('servings')
        if not is_positive_number(servings):
            self._my_errors['servings'].append(
                'Servings must be a positive number'
            )
        return servings
