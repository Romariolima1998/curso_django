from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_browser
from recipes.tests.test_recipe_base import RecpeMixin


class RecipeBaseFunctionalTest(StaticLiveServerTestCase, RecpeMixin):
    def setUp(self):
        self.browser = make_chrome_browser('--headless')
        self.browser.implicitly_wait(10)
        return super().setUp()

    def tearDown(self):
        self.browser.quit()
        return super().tearDown()