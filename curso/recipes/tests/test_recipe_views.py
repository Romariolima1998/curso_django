from django.urls import reverse, resolve

from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase


class Recipe_view_test(RecipeTestBase):
    def test_recipe_home_views_function_is_correct(self):
        view = resolve(reverse('recipes:home'))

        self.assertIs(view.func, views.home)

    def test_recipe_detail_views_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', args=(1,)))

        self.assertIs(view.func, views.recipe)

    def test_recipe_category_views_function_is_correct(self):
        view = resolve(reverse('recipes:category', args=(1,)))

        self.assertIs(view.func, views.category)

    def test_recipe_home_return_status_code_200(self):
        response = self.client.get(reverse('recipes:home'))

        self.assertEqual(response.status_code, 200)

    def test_recipe_home_loads_corrects_templates(self):
        response = self.client.get(reverse('recipes:home'))

        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_no_recipe_found_here_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))

        self.assertIn('No recipes found here!', response.content.decode('utf-8'))
    
    def test_recipe_category_return_status_code_404_if_not_recipe(self):
        response = self.client.get(reverse('recipes:category', args=(1,)))

        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_return_status_code_404_if_not_recipe(self):
        response = self.client.get(reverse('recipes:recipe', args=(1,)))

        self.assertEqual(response.status_code, 404)

    def test_recipe_home_loads_recipes(self):
        

        response = self.client.get(reverse('recipes:home'))
        response_content = response.content.decode('utf-8')

        self.assertIn('recipe title', response_content)
