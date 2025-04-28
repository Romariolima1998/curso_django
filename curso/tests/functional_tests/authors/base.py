from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_browser

from selenium.webdriver.common.by import By


class AuthorsBaseTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self):
        self.browser.quit()
        return super().tearDown()

    def get_by_placeholder(self, form, placeholder):
        return form.find_element(By.XPATH, f'//input[@placeholder="{placeholder}"]')

    
