class PropertyLinksStructure:
    def __init__(self, element, price_elem, page):
        self.url = element.get_attribute('href')
        self.page = page
        self.price = self._get_price(element=price_elem)
        self.property_id = self._get_property_id()

    def _get_property_id(self):
        return self.url.split("/")[-1]

    @staticmethod
    def _get_price(element):
        return element.text.strip('.–').strip('CHF\n').replace(',', '').strip('EUR\n')

    def get_property_data_dict(self):
        return {
            'property_id': self.property_id,
            'price': self.price,
            'url': self.url,
            'page': self.page,
        }
