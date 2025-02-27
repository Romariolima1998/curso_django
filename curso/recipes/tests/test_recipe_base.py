from django.test import TestCase

from recipes.models import Category, Recipe, User


class RecipeTestBase(TestCase):
    def setUp(self):
        category = Category.objects.create(name='category')

        author = User.objects.create_user(
            first_name='user',
            username='user',
            password='user',
            email='user@email.com'
        )

        recipe = Recipe.objects.create(
            author=author,
            category=category,
            title='recipe title',
            description='recipe description',
            slug='recipe slug',
            preparation_time=10,
            preparation_time_unit='minutos',
            servings=5,
            servings_unit='poecoes',
            preparation_steps='recipe preparations steps',
            preparation_steps_is_html=False,
            is_published=True,
        )
        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()