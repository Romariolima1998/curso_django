from django.test import TestCase

from recipes.models import Category, Recipe, User


class RecpeMixin:
    def make_category(self, name='category'):
        return Category.objects.create(name=name)

    def make_author(
            self,
            first_name='user',
            username='user',
            password='user',
            email='user@email.com'
    ):
        return User.objects.create_user(
            first_name=first_name,
            username=username,
            password=password,
            email=email
        )

    def make_recipe(
            self,
            author_data=None,
            category_data=None,
            title='recipe title',
            description='recipe description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='minutos',
            servings=5,
            servings_unit='poecoes',
            preparation_steps='recipe preparations steps',
            preparation_steps_is_html=False,
            is_published=True,
            ):

        if author_data is None:
            author_data = {}

        if category_data is None:
            category_data = {}

        return Recipe.objects.create(
            author=self.make_author(**author_data),
            category=self.make_category(**category_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
        )

    def make_recipe_no_default(self):
        return Recipe(
            author=self.make_author(username='newuser'),
            category=self.make_category(name='test default category'),
            title='recipe title',
            description='recipe description',
            slug='recipe-slug-no-defalt',
            preparation_time=10,
            preparation_time_unit='minutos',
            servings=5,
            servings_unit='poecoes',
            preparation_steps='recipe preparations steps',
        )

    def make_recipe_in_batch(self, count=10):
        recipes = []
        for i in range(9):
            kwargs = {
                'title': f'recipe title {i}',
                'author_data': {'username': f'author{i}'},
                'slug': f'slug-{i}',
            }
            recipes.append(self.make_recipe(**kwargs))
        return recipes

class RecipeTestBase(TestCase, RecpeMixin):
    ...
    