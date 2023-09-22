from typing import Dict

import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import undetected_chromedriver as uc

from src.get_real_estate_data.links_scraper.property_links_structure import PropertyLinksStructure
from src.get_real_estate_data.helper.webscraping_helper import WebscrapingHelper


class PropertyLinksScraper(WebscrapingHelper):
    def __init__(
            self,
            driver: uc,
            page_url: str,
            elems_path: Dict,
            helper_path: Dict,
            canton_name: str = '',
            no_pages_to_scrape: int = 100,
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
        self.canton_name = canton_name
        self.no_pages_to_scrape = no_pages_to_scrape
        self.no_pages_after_delete_cookies = no_pages_after_delete_cookies

        self.all_urls = []
        self.page_number = 0

    def _get_property_urls(self) -> None:
        properties = self.driver.find_elements(By.CSS_SELECTOR, self.elems_path['property'])
        self.page_number += 1

        for prop in properties:
            try:
                price = self._find_element_in_property(prop, self.elems_path['price'])
                rooms = self._find_element_in_property(prop, self.elems_path['rooms'])
                living_space = self._find_element_in_property(prop, self.elems_path['living_space'])
                address = self._find_element_in_property(prop, self.elems_path['address'])
                text = self._find_element_in_property(prop, self.elems_path['text'])
                image = self._find_element_in_property(prop, self.elems_path['image'])

                property_obj = PropertyLinksStructure(
                    element=prop,
                    price_elem=price,
                    rooms_elem=rooms,
                    living_space_elem=living_space,
                    address_elem=address,
                    text_elem=text,
                    image_elem=image,
                    page=self.page_number,
                )
                self.all_urls.append(property_obj.get_property_data_dict())
            except Exception as e:
                print(f"Error occurred while processing a property: {e}")
            time.sleep(3)

    @staticmethod
    def _find_element_in_property(property_element, css_selector):
        try:
            return property_element.find_element(By.CSS_SELECTOR, css_selector)
        except NoSuchElementException:
            return None

    def _go_to_next_page(self) -> None:
        """
        Navigate to the next page.
        """
        next_link = WebDriverWait(self.driver, 3).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, self.elems_path['next_page']))
        )
        next_link.click()
        time.sleep(6)

    def _save_data(self) -> pd.DataFrame:
        """
        Save the scraped data to a CSV file with the canton name.
        """
        df = pd.DataFrame(self.all_urls)
        today = str(pd.to_datetime('today').normalize().date())
        file_name = f"{self.canton_name}_urls_{today}.csv"
        df.to_csv(file_name, index=False, encoding="utf-8")
        print(f"Data saved to {file_name}")
        return df

    def _clear_cache_and_cookies_if_needed(self) -> None:
        """
        Clear cache and cookies if the specified number of pages has been scraped.
        """
        if self.page_number % self.no_pages_after_delete_cookies == 0:
            self.delete_cache()
            self.delete_cookies_and_refresh()

    def scrape_data(self) -> pd.DataFrame:
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
                    df = self._save_data()
                    self.driver.quit()
                    break
            except TimeoutException:
                print("TimeoutException occurred. Saving get_real_estate_data and stopping the script...")
                df = self._save_data()
                self.driver.quit()
                break
            except Exception as e:
                print(f"Error occurred while scraping page {self.page_number}: {e}")
                print("Saving scraped data so far to 'incomplete_urls.csv'")
                self._save_data()
                print("Data saved. Continuing with the next page.")
                self._go_to_next_page()

        return df
