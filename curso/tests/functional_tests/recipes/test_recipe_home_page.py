import time

# from django.test import LiveServerTestCase
# from selenium.webdriver.chrome.service import Service

from unittest.mock import patch
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from curso.tests.functional_tests.recipes.base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_home_page_without_recipes_error_messages(self):

        # Given I have a home page
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')

        self.assertIn(
            'No recipes found here!',
            body.text
        )

    def test_recipe_search_input_can_find_correct_recipes(self):

        recipes = self.make_recipe_in_batch()
        self.browser.get(self.live_server_url)

        search_input = self.browser.find_element(By.XPATH, '//input[@placeholder="search for a recipes"]')

        search_input.send_keys(recipes[0].title)

        search_input.send_keys(Keys.ENTER)
        time.sleep(2)

        body = self.browser.find_element(By.CLASS_NAME, 'main-content-list')
        self.assertIn(
            recipes[0].title,
            body.text
        )

    @patch('recipes.views.PER_PAGES', new=2)
    def test_recipe_home_page_pagination(self):
        # Given I have a home page with 20 recipes
        self.make_recipe_in_batch()
        self.browser.get(self.live_server_url)

        # ver que tem uma paginacao e clica na pagine 2
        page2 = self.browser.find_element(By.XPATH, '//a[@aria-label="go to page 2"]')

        page2.click()

        # Ver a quantidade de receitas na pagina 2
        body = self.browser.find_elements(By.CLASS_NAME, 'recipe')
        self.assertEqual(
            len(body),
            2
        )
