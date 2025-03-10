from django.urls import reverse, resolve

from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase


class RecipeDetailviewtest(RecipeTestBase):
    
    def test_recipe_detail_views_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', args=(1,)))

        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_return_status_code_404_if_not_recipe(self):
        response = self.client.get(reverse('recipes:recipe', args=(1,)))

        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_loads_correct_recipe(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:recipe', args=(1,)))
        response_content = response.content.decode('utf-8')

        self.assertIn('recipe title', response_content)

    def test_recipe_detail_not_loads_correct_recipe_if_is_published_false(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:recipe', args=(recipe.id,)))

        self.assertEqual(response.status_code, 404)
