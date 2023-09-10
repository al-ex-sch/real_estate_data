from typing import Dict

import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import undetected_chromedriver as uc

from src.get_real_estate_data.links_scraper.property_links_structure import PropertyLinksStructure
from src.get_real_estate_data.shared.webscraping_helper import WebscrapingHelper


class PropertyLinksScraper(WebscrapingHelper):
    def __init__(
            self,
            driver: uc,
            page_url: str,
            elems_path: Dict,
            helper_path: Dict,
            no_pages_to_scrape: int = 1000,
    ):
        super().__init__(driver=driver, helper_paths=helper_path)
        self.page_url = page_url
        self.elems_path = elems_path
        self.no_pages_to_scrape = no_pages_to_scrape

        self.all_urls = []
        self.page_number = 0

    def _get_property_urls(self) -> None:
        properties = self.driver.find_elements(By.CSS_SELECTOR, self.elems_path['property'])
        prices = self.driver.find_elements(By.CSS_SELECTOR, self.elems_path['price'])
        self.page_number += 1
        for prem, price in zip(properties, prices):
            property_obj = PropertyLinksStructure(
                element=prem, price_elem=price, page=self.page_number,
            )
            self.all_urls.append(property_obj.get_property_data_dict())

    def _go_to_next_page(self) -> None:
        next_link = WebDriverWait(self.driver, 4).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, self.elems_path['next_page']))
        )
        next_link.click()
        time.sleep(6)

    def _save_data(self) -> None:
        df = pd.DataFrame(self.all_urls)
        today = str(pd.to_datetime('today').normalize().date())
        df.to_csv(f'urls_{today}.csv', index=False)
        print(f"Data saved to urls_{today}.csv")

    def scrape_data(self) -> None:
        self.load_page(self.page_url)
        while True:
            try:
                self._get_property_urls()
                self._go_to_next_page()
                if self.page_number >= self.no_pages_to_scrape:
                    print(
                        f"Reached the maximum number of pages ({self.no_pages_to_scrape}). "
                        f"Saving get_real_estate_data & stopping the script..."
                    )
                    self._save_data()
                    self.driver.quit()
                    break
            except TimeoutException:
                print("TimeoutException occurred. Saving get_real_estate_data and stopping the script...")
                self._save_data()
                self.driver.quit()
                break
