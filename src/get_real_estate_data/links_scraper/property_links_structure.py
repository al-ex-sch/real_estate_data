from typing import Dict

from selenium.webdriver.remote.webelement import WebElement


class PropertyLinksStructure:
    def __init__(self, element: WebElement, price_elem: WebElement, page):
        """
        A class to represent the structure of property links.

        :param element: A WebElement containing the property link.
        :param price_elem: A WebElement containing the property price.
        :param page: The page number where the property is found.
        """
        self.url = element.get_attribute('href')
        self.page = page
        self.price = self._get_price(element=price_elem)
        self.property_id = self._get_property_id()

    def _get_property_id(self) -> str:
        """
        Extract the property ID from the property URL.
        :return: The property ID.
        """
        return self.url.split("/")[-1]

    @staticmethod
    def _get_price(element: WebElement) -> str:
        """
        Extract the price from the given WebElement.
        :param element: A WebElement containing the property price.
        :return: The property price as a string.
        """
        return element.text.strip('.–').strip('CHF\n').replace(',', '').strip('EUR\n')

    def get_property_data_dict(self) -> Dict:
        """
        Return the property data as a dictionary.
        :return: A dictionary containing the property ID, price, URL, and page number.
        :rtype: Dict
        """
        return {
            'property_id': self.property_id,
            'price': self.price,
            'url': self.url,
            'page': self.page,
        }
