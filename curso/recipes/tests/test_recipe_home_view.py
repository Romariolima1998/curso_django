from django.urls import reverse, resolve

from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase


class RecipeHomeviewtest(RecipeTestBase):
    def test_recipe_home_views_function_is_correct(self):
        view = resolve(reverse('recipes:home'))

        self.assertIs(view.func, views.home)

    def test_recipe_home_return_status_code_200(self):
        response = self.client.get(reverse('recipes:home'))

        self.assertEqual(response.status_code, 200)

    def test_recipe_home_loads_corrects_templates(self):
        response = self.client.get(reverse('recipes:home'))

        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_no_recipe_found_here_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))

        self.assertIn('No recipes found here!', response.content.decode('utf-8'))

    def test_recipe_home_loads_recipes(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        response_content = response.content.decode('utf-8')

        self.assertIn('recipe title', response_content)

    def test_recipe_home_not_loads_recipes_if_is_published_false(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        response_content = response.content.decode('utf-8')

        self.assertNotIn('recipe title', response_content)