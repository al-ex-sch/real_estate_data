import re
import time
import datetime
from typing import Dict, Union, List

import pandas as pd
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import undetected_chromedriver as uc

from src.get_real_estate_data.listings_scraper.data_cleaner import DataCleaner
from src.get_real_estate_data.listings_scraper.features_split import SplitFeatures
from src.get_real_estate_data.shared.webscraping_helper import WebscrapingHelper


class IndividualListingsScraper(WebscrapingHelper):
    def __init__(
            self,
            driver: uc,
            elems_path: Dict,
            imgs_path: Dict,
            helper_path: Dict,
            no_links_after_delete_cookies: int = 10,
    ):
        """
        Scrape property listings details from a real estate website based on previously scraped links.

        :param driver: the undetected_chromedriver instance
        :param elems_path: Dict containing property details paths for scraping
        :param imgs_path: Dict containing image paths for scraping
        :param helper_path: Dict containing helper paths for scraping
        :param no_links_after_delete_cookies: int, number of links to process before deleting cookies and cache
        """
        super().__init__(driver=driver, helper_paths=helper_path)
        self.elems_path = elems_path
        self.imgs_path = imgs_path
        self.no_links_after_delete_cookies = no_links_after_delete_cookies
        self.data_cleaner_class = DataCleaner

    @staticmethod
    def _get_links_and_existing_info(row: pd.Series, df: pd.DataFrame) -> Dict:
        """
        Get the links and existing information from a row in the DataFrame.

        :param row: pd.Series, the row to extract information from
        :param df: pd.DataFrame, the DataFrame containing rows
        :return: Dict, dictionary containing extracted links and existing information
        """
        existing_info_dict = {'link': row['url']}
        for column in df.columns:
            if column != 'url':
                existing_info_dict[column] = row[column]
        return existing_info_dict

    @staticmethod
    def _handle_unavailable_property(existing_info_dict: Dict) -> Dict:
        """
        Handle the case when a property is unavailable.

        :param existing_info_dict: Dict containing existing information from the links scraping
        :return: Dict, updated with the property marked as unavailable
        """
        existing_info_dict['deleted'] = datetime.date.today().strftime('%Y-%m-%d')
        return existing_info_dict

    def _clear_cache_and_cookies_if_needed(self, counter: int):
        """
        Clear cache and cookies if the counter reaches the specified number of links.

        :param counter: int, the counter for processed links
        """
        if counter % self.no_links_after_delete_cookies == 0:
            self.delete_cache()
            self.delete_cookies_and_refresh()

    def _get_image_links(self, images_path: str, button_path: str, img_count_paths: List[str]) -> List[str]:
        """
        Get image links for a property.

        :param images_path: str, the path to the image elements
        :param button_path: str, the path to the button element for loading images
        :param img_count_paths: List[str], list of paths to image count elements
        :return: List[str], list of image links
        """
        img_count_element = None

        try:
            img_count_element = self.driver.find_element(By.XPATH, img_count_paths[0])
        except NoSuchElementException:
            pass

        if not img_count_element:
            try:
                img_count_element = self.driver.find_element(By.XPATH, img_count_paths[1])
            except NoSuchElementException:
                pass

        if img_count_element:
            num_images = int(re.search(r'\d+', img_count_element.text).group())
            button_element = None

            try:
                button_element = self.driver.find_element(By.CSS_SELECTOR, button_path)
            except NoSuchElementException:
                pass

            if button_element:
                for _ in range(num_images):
                    button_element.click()
                    time.sleep(1)

            image_elements = self.driver.find_elements(By.CSS_SELECTOR, images_path)
            image_links = [element.get_attribute('src') for element in image_elements if element]
            return list(set(image_links))

        return []

    def _extract_direct_text(self, path: str) -> str:
        """
        Extract direct text from an element.

        :param path: str, the path to the element
        :return: str, the extracted text
        """
        element = self.driver.find_element(By.CSS_SELECTOR, path)
        return element.text if element else 'n/a'

    def _extract_multiple_elements(self, path: str) -> List[str]:
        """
        Extract multiple elements from a path.

        :param path: str, the path to the elements
        :return: List[str], list of extracted elements
        """
        elements = self.driver.find_elements(By.CSS_SELECTOR, path)
        return [element.get_attribute('src') for element in elements if element]

    def _extract_element_text(self, path: str) -> str:
        """
        Extract text from an element.

        :param path: str, the path to the element
        :return: str, the extracted text
        """
        elements = self.driver.find_elements(By.CSS_SELECTOR, path)
        return elements[0].text if elements else 'n/a'

    def _extract_data(self, key: str, path: str) -> Union[List, str]:
        """
        Extract get_real_estate_data from a path based on the key.

        :param key: str, the key indicating the type of get_real_estate_data to extract
        :param path: str, the path to the element
        :return: Union[List, str], the extracted get_real_estate_data
        """
        direct_text = key == 'address'
        if direct_text:
            return self._extract_direct_text(path)
        elif key == 'image_links':
            return self._extract_multiple_elements(path)
        else:
            return self._extract_element_text(path)

    def _loop_through_all_paths_and_clean(
            self, existing_info_dict: Dict, row: pd.Series, counter: int,
    ) -> Dict:
        """
        Loop through all paths, extract and clean the get_real_estate_data.

        :param existing_info_dict: Dict, the dictionary containing existing information
        :param row: pd.Series, the row to process
        :param counter: int, the counter for processed links
        :return: Dict, updated dictionary with cleaned get_real_estate_data
        """
        self.driver.get(row['url'])

        if not self.driver.find_elements(By.CSS_SELECTOR, self.helper_paths['detect_unavailable_prop']):
            return self._handle_unavailable_property(existing_info_dict)

        self._clear_cache_and_cookies_if_needed(counter)

        for key, path in self.elems_path.items():
            if key == 'image_links':
                existing_info_dict[key] = self._get_image_links(
                    images_path=path,
                    button_path=self.imgs_path['load_images_button'],
                    img_count_paths=[
                        self.imgs_path['image_count_1'],
                        self.imgs_path['image_count_2'],
                    ],
                )
            else:
                direct_text = key == 'address'
                extracted_text = self._extract_data(key=direct_text, path=path)
                data_cleaner = self.data_cleaner_class(key, extracted_text)
                cleaned_text = data_cleaner.clean()
                existing_info_dict[key] = cleaned_text

        return existing_info_dict

    @staticmethod
    def save_df_to_csv(df: pd.DataFrame, file_name: str) -> None:
        """
        Save the input DataFrame to a CSV file with the given file name and today's date.

        :param df: pd.DataFrame, the DataFrame to be saved
        :param file_name: str, the base file name for the CSV file
        """
        today = str(pd.to_datetime("today").normalize().date())
        file_name_with_date = f"{file_name}_{today}.csv"
        df.to_csv(file_name_with_date, index=False, encoding="utf-8")

    def scrape_all_properties(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Scrape all properties in the given DataFrame.

        :param df: pd.DataFrame, the DataFrame containing property URLs
        :return: pd.DataFrame, the DataFrame containing scraped get_real_estate_data
        """
        self.driver.maximize_window()
        rows = df.iterrows()

        listings_details = []

        total_properties = len(df)
        for counter, (_, row) in enumerate(rows):
            property_id = row["url"].split("/")[-1]
            print(f"Scraping property {property_id} ({counter + 1} out of {total_properties})")

            try:
                existing_info_dict = self._get_links_and_existing_info(row=row, df=df)
                info_dict = self._loop_through_all_paths_and_clean(
                    existing_info_dict=existing_info_dict, row=row, counter=counter,
                )
                listings_details.append(info_dict)
            except Exception as e:
                print(f"Error occurred while scraping property {property_id}: {e}")
                print("Saving scraped properties so far to 'incomplete_listings_details.csv'")
                scraped_properties_df = pd.DataFrame(listings_details)
                self.save_df_to_csv(scraped_properties_df, "uncompleted_properties_details")
                print("Data saved. Continuing with the next property.")

            time.sleep(4)

        listings_details_df = pd.DataFrame(listings_details)

        split_features = SplitFeatures()
        processed_df = split_features.process_data(listings_details_df)

        self.save_df_to_csv(processed_df, "listings_details")

        return processed_df
