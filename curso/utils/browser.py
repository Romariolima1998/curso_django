from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

ROOT_DIR = Path(__file__).parent.parent

CHROMEDRIVER_NAME = 'chromedriver'
CHROMEDRIVER_PATH = ROOT_DIR / 'bin' / CHROMEDRIVER_NAME


def make_chrome_browser(*option):
    chrome_options = webdriver.ChromeOptions()
    if option:
        for opt in option:
            chrome_options.add_argument(opt)
    chrome_service = Service(executable_path=str(CHROMEDRIVER_PATH))

    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)

    return browser


if __name__ == '__main__':
    browser = make_chrome_browser()
    browser.get('https://www.google.com')
    browser.implicitly_wait(10)  # seconds
    browser.quit()
