import math
from typing import List, Dict

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By


class LinkGenerator:
    def __init__(self, cantons_list: List, canton_dict: Dict):
        self.cantons_list = cantons_list
        self.canton_dict = canton_dict

    def get_original_links(self):
        base_url = "https://www.homegate.ch/buy/apartment/canton-"
        css_selector = "span.ResultsNumber_results_zTgsG.ResultListHeader_locations_zQj9c"
        original_links = []

        my_driver = uc.Chrome()

        for canton in self.cantons_list:
            url = f"{base_url}{canton}/matching-list?ipd=true"
            my_driver.get(url)
            results_text = my_driver.find_element(By.CSS_SELECTOR, css_selector).text
            results_number = int(results_text.split(" ")[0])

            if results_number < 1000:
                original_links.append(url)
            else:
                links_count = math.ceil(results_number / 1000)
                print(f"Canton {canton} has {links_count} links and {results_number} results.")

        my_driver.quit()

        return original_links

    def generate_all_links(self):
        all_links = []

        for canton, values in self.canton_dict.items():
            base_url = f"https://www.homegate.ch/buy/house/canton-{canton}/matching-list?ipd=true"

            values.insert(0, 0)

            for i in range(1, len(values) + 1):
                ai = values[i - 1] + 1 if i > 1 else ''
                aj = values[i] if i < len(values) else ''

                new_link = f"{base_url}&ai={ai}&aj={aj}"
                all_links.append(new_link)

        return all_links

    def get_all_links(self):
        original_links = self.get_original_links()
        generated_links = self.generate_all_links()
        return original_links + generated_links
