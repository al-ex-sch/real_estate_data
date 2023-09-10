import time
from typing import Dict

from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import undetected_chromedriver as uc


class WebscrapingHelper:
    def __init__(self, driver: uc, helper_paths: Dict):
        self.driver = driver
        self.helper_paths = helper_paths

    def delete_cache(self):
        self.driver.execute_script("window.localStorage.clear();")
        self.driver.execute_script("window.sessionStorage.clear();")
        self.driver.execute_script(
            "window.indexedDB.deleteDatabase('chrome-extension_kbmfpngjjgdllneeigpgjifpgocmfgmb');"
        )
        self.driver.execute_script("window.indexedDB.deleteDatabase('_manifest');")

    def click_cookies_button(self):
        cookies = WebDriverWait(self.driver, 20).until(
            ec.presence_of_element_located((By.XPATH, self.helper_paths['cookies']))
        )
        cookies.click()

    def load_page(self, page_url):
        self.driver.maximize_window()
        self.driver.get(page_url)
        self.click_cookies_button()

    def delete_cookies_and_refresh(self):
        if self.driver.current_url:
            self.driver.delete_all_cookies()
            self.driver.refresh()
            time.sleep(5)
            try:
                self.click_cookies_button()
            except TimeoutException:
                pass
