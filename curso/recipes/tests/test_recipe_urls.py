from django.test import TestCase
from django.urls import reverse


class RecipeUrlsTest(TestCase):

    def test_recipe_home_url_is_correct(self):
        home_url = reverse('recipes:home')

        self.assertEqual(home_url, '/')

    def test_recipe_category_url_is_correct(self):
        category_url = reverse('recipes:category', args=(1,))

        self.assertEqual(category_url, '/recipe/category/1/')

    def test_recipe_detail_url_is_correct(self):
        category_url = reverse('recipes:recipe', args=(1,))

        self.assertEqual(category_url, '/recipe/1/')
