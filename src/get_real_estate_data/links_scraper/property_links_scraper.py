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
            no_pages_after_delete_cookies: int = 10,
    ):
        """
        Scrape property links from a real estate website.

        :param driver: A selenium webdriver instance.
        :param page_url: The URL of the page to start scraping from.
        :param elems_path: A dictionary containing the CSS selectors for the elements to be scraped.
        :param helper_path: A dictionary containing helper paths for the WebscrapingHelper.
        :param no_pages_to_scrape: The maximum number of pages to scrape, defaults to 1000.
        :param no_pages_after_delete_cookies: The number of pages to scrape before deleting cookies and cache.
        """
        super().__init__(driver=driver, helper_paths=helper_path)
        self.page_url = page_url
        self.elems_path = elems_path
        self.no_pages_to_scrape = no_pages_to_scrape
        self.no_pages_after_delete_cookies = no_pages_after_delete_cookies

        self.all_urls = []
        self.page_number = 0

    def _get_property_urls(self) -> None:
        """
        Extract property URLs from the current page.
        """
        properties = self.driver.find_elements(By.CSS_SELECTOR, self.elems_path['property'])
        prices = self.driver.find_elements(By.CSS_SELECTOR, self.elems_path['price'])
        self.page_number += 1
        for prem, price in zip(properties, prices):
            property_obj = PropertyLinksStructure(
                element=prem, price_elem=price, page=self.page_number,
            )
            self.all_urls.append(property_obj.get_property_data_dict())

    def _go_to_next_page(self) -> None:
        """
        Navigate to the next page.
        """
        next_link = WebDriverWait(self.driver, 4).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, self.elems_path['next_page']))
        )
        next_link.click()
        time.sleep(6)

    def _save_data(self) -> None:
        """
        Save the scraped data to a CSV file.
        """
        df = pd.DataFrame(self.all_urls)
        today = str(pd.to_datetime('today').normalize().date())
        df.to_csv(f'urls_{today}.csv', index=False)
        print(f"Data saved to urls_{today}.csv")

    def _clear_cache_and_cookies_if_needed(self) -> None:
        """
        Clear cache and cookies if the specified number of pages has been scraped.
        """
        if self.page_number % self.no_pages_after_delete_cookies == 0:
            self.delete_cache()
            self.delete_cookies_and_refresh()

    def scrape_data(self) -> None:
        """
        Perform the data scraping process.
        It will scrape property URLs and navigate through pages until the maximum number of pages is reached
        or a TimeoutException occurs.
        """
        self.load_page(self.page_url)
        while True:
            try:
                print(f"Scraping page {self.page_number}")
                self._get_property_urls()
                self._clear_cache_and_cookies_if_needed()
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
            except Exception as e:
                print(f"Error occurred while scraping page {self.page_number}: {e}")
                print("Saving scraped data so far to 'incomplete_urls.csv'")
                self._save_data()
                print("Data saved. Continuing with the next page.")
                self._go_to_next_page()
