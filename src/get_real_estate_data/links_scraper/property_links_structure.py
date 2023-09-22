from typing import Dict

from selenium.webdriver.remote.webelement import WebElement


class PropertyLinksStructure:
    def __init__(
            self,
            element: WebElement,
            price_elem: WebElement,
            rooms_elem: WebElement,
            living_space_elem: WebElement,
            address_elem: WebElement,
            text_elem: WebElement,
            image_elem: WebElement,
            page,
    ):
        self.url = self._get_element_attribute(element, 'href')
        self.page = page
        self.price = self._process_price(price_elem)
        self.rooms = self._get_text(element=rooms_elem)
        self.living_space = self._process_living_space(living_space_elem)
        self.address = self._get_text(element=address_elem)
        self.text = self._get_text(element=text_elem)
        self.image_url = self._get_element_attribute(image_elem, 'src')
        self.property_id = self._get_property_id() if self.url else None

    @staticmethod
    def _get_element_attribute(element, attribute):
        return element.get_attribute(attribute) if element else None

    def _process_price(self, price_elem):
        price_text = self._get_text(element=price_elem)
        if price_text:
            return price_text.strip('.–').strip('CHF\n').replace(',', '').strip('EUR\n')
        return None

    def _process_living_space(self, living_space_elem):
        living_space_text = self._get_text(element=living_space_elem)
        if living_space_text:
            return living_space_text.strip('\nm2')
        return None

    def _get_property_id(self) -> str:
        """
        Extract the property ID from the property URL.
        :return: The property ID.
        """
        return self.url.split("/")[-1]

    @staticmethod
    def _get_text(element: WebElement) -> str:
        """
        Extract the text from the given WebElement.
        :param element: A WebElement containing the text.
        :return: The text as a string.
        """
        return element.text.strip() if element else None

    def get_property_data_dict(self) -> Dict:
        return {
            'property_id': self.property_id,
            'price': self.price,
            'rooms': self.rooms,
            'living_space': self.living_space,
            'address': self.address,
            'text': self.text,
            'image_url': self.image_url,
            'link': self.url,
            'page': self.page,
        }
