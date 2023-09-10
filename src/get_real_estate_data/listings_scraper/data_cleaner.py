class DataCleaner:
    def __init__(self, key, text):
        self.key = key
        self.text = text

    def clean(self):
        if hasattr(self, f"clean_{self.key}"):
            return getattr(self, f"clean_{self.key}")()
        else:
            return self.text

    def clean_address(self):
        return self.text

    def clean_no_rooms(self):
        return self.text

    def clean_living_area(self):
        return self.text.strip('\nm2')

    def clean_main_info(self):
        return self.text.strip('Main information\n').replace('\n', ', ').replace(':,', ':')

    def clean_features_furnishings(self):
        return self.text.replace('\n', ', ')

    def clean_description(self):
        return self.text.strip('Description\n ').replace('\n', ' ')

    def clean_advertiser(self):
        return self.text

    def clean_title(self):
        return self.text.strip('"')
