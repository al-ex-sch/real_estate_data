class DataCleaner:
    def __init__(self, key: str, text: str):
        """
        A class used to clean the text data of various attributes in a dataset.

        :param key: The key representing the attribute to be cleaned.
        :param text: The text data to be cleaned.
        """
        self.key = key
        self.text = text

    def clean(self) -> str:
        """
        Apply the appropriate cleaning method based on the attribute key.

        :return: Cleaned text data.
        """
        if hasattr(self, f"clean_{self.key}"):
            return getattr(self, f"clean_{self.key}")()
        else:
            return self.text

    def clean_address(self) -> str:
        return self.text

    def clean_no_rooms(self) -> str:
        return self.text

    def clean_living_area(self) -> str:
        return self.text.strip('\nm2')

    def clean_main_info(self) -> str:
        return self.text.strip('Main information\n').replace('\n', ', ').replace(':,', ':')

    def clean_features_furnishings(self) -> str:
        return self.text.replace('\n', ', ')

    def clean_description(self) -> str:
        return self.text.strip('Description\n ').replace('\n', ' ')

    def clean_advertiser(self) -> str:
        return self.text

    def clean_title(self) -> str:
        return self.text.strip('"')
