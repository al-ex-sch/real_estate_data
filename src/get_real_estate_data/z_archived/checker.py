##
import os
import re
import time

import pandas as pd
import undetected_chromedriver as uc
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from src.get_real_estate_data.a_helper.config import scrape_links_houses, scrape_links_buy


class HomegateChecker:
    def __init__(self, links, driver, file_path):
        self.links = links
        self.driver = driver
        self.file_path = file_path

    @staticmethod
    def get_canton_name(link):
        return re.search(r'canton-([\w-]+)', link).group(1)

    def find_corresponding_file(self, canton_name):
        files = [f for f in os.listdir(self.file_path) if f.startswith(f"canton-{canton_name}")]  # canton-canton. (for house buy)
        return os.path.join(self.file_path, files[0]) if files else None

    def get_max_page_from_element(self, link):
        self.driver.get(link)
        time.sleep(5)
        try:
            element = self.driver.find_element(
                By.XPATH,
                '//*[@id="app"]/main/div/div[2]/div/div[5]/div[3]/nav/a[3]/span'
            )
            return int(element.text.strip('...'))
        except NoSuchElementException:
            print(f"Element for the canton {self.get_canton_name(link)} was not found")
            return None

    def check_max_page(self, link, filename):
        canton_name = self.get_canton_name(link)
        max_page = self.get_max_page_from_element(link)
        if max_page:
            df = pd.read_csv(filename)
            max_page_in_file = df['page'].max()
            if max_page != max_page_in_file:
                print(
                    f"Max page in file ({max_page_in_file}) does not match max page in element ({max_page}) "
                    f"for canton {canton_name}"
                )
            else:
                return df

    def process_dataframe(self, df, canton_name):
        df_filtered = df[df['price'].notnull()]
        grouped = df_filtered.groupby('page').size()
        for page, count in grouped.items():
            if count != 20 and page != grouped.index.max():
                print(f"Page {page} has {count} elements instead of 20 for canton {canton_name}")

    def run(self):
        for link in self.links:
            canton_name = self.get_canton_name(link)
            filename = self.find_corresponding_file(canton_name)
            if filename:
                df = self.check_max_page(link, filename)
                if df is not None:
                    self.process_dataframe(df, canton_name)
            else:
                print(f"No file found for canton {canton_name}")


driver = uc.Chrome()
file_path = '/2023-09-23 apartments buy'
checker = HomegateChecker(scrape_links_buy, driver, file_path)
checker.run()
driver.quit()
