from django.urls import reverse, resolve

from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase


class RecipeSearchviewtest(RecipeTestBase):

    def test_recipe_search_uses_correct_view_function(self):
        view = resolve(reverse('recipes:search'))

        self.assertIs(view.func.view_class, views.SearchListView)

    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=teste')

        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_terms(self):
        response = self.client.get(reverse('recipes:search'))

        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_scape(self):
        response = self.client.get(reverse('recipes:search') + '?q=<test>')

        self.assertIn('Search for &quot;&lt;test&gt;&quot;', response.content.decode('utf-8'))

    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'this one'
        title2 = 'this two'

        recipe1 = self.make_recipe(
            slug='one',
            title=title1,
            author_data={'username': 'one'})
        
        recipe2 = self.make_recipe(
            slug='two',
            title=title2,
            author_data={'username': 'two'}
            )

        response1 = self.client.get(reverse('recipes:search') + f'?q={title1}')
        response2 = self.client.get(reverse('recipes:search') + f'?q={title2}')
        response_both = self.client.get(reverse('recipes:search') + '?q=this')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])