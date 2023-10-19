links_paths = {
    'property': 'a.HgCardElevated_link_OMJcD',
    'price': 'span.HgListingCard_price_sIIoV',
    'rooms': 'div.HgListingRoomsLivingSpace_roomsLivingSpace_FiW9E > span:nth-child(1) > strong',
    'living_space': 'div.HgListingRoomsLivingSpace_roomsLivingSpace_FiW9E > span:nth-child(2) > strong',
    'address': 'div.HgListingCard_address_dbLZ8 > address',
    'text': 'div.HgListingDescription_description_SoeAa',
    'image': 'li.glide__slide.glide__slide--active > picture > img',
    'next_page': 'a:nth-child(7)',
}

paths_helper = {
    'cookies': '//*[@id="onetrust-accept-btn-handler"]',
    'hover': 'a:nth-child(7)',
    'detect_unavailable_prop': 'div.SpotlightAttributesPrice_value_TqKGz',
}

cantons = [
    'zurich', 'bern', 'lucerne', 'uri', 'schwyz', 'obwalden', 'nidwalden', 'glarus', 'zug', 'fribourg', 'solothurn',
    'baselstadt', 'baselland', 'schaffhausen', 'appenzellausserrhoden', 'appenzellinnerrhoden', 'stgallen',
    'graubuenden', 'aargau', 'thurgau', 'ticino', 'vaud', 'valais', 'neuchatel', 'geneva', 'jura',
]

cantons_split_apartments = {
    'zurich': [1400000],
    'aargau': [1400000],
    'ticino': [450000, 600000, 800000, 1200000, 2000000],
    'vaud': [850000, 1500000],
    'valais': [450000, 600000, 800000],
}

cantons_split_apartments_rent = {
    'bern': [1400, 1800],
    'zurich': [2100, 3000],
    'solothurn': [1600],
    'baselland': [1900],
    'stgallen': [1500],
    'aargau': [1700],
    'ticino': [1300, 2000],
    'vaud': [2000],
}

scrape_links = [
    'https://www.homegate.ch/buy/apartment/canton-bern/matching-list?ipd=true',
    'https://www.homegate.ch/buy/apartment/canton-lucerne/matching-list?ipd=true',
    'https://www.homegate.ch/buy/apartment/canton-uri/matching-list?ipd=true',
    'https://www.homegate.ch/buy/apartment/canton-schwyz/matching-list?ipd=true',
    'https://www.homegate.ch/buy/apartment/canton-obwalden/matching-list?ipd=true',
    'https://www.homegate.ch/buy/apartment/canton-nidwalden/matching-list?ipd=true',
    'https://www.homegate.ch/buy/apartment/canton-glarus/matching-list?ipd=true',
    'https://www.homegate.ch/buy/apartment/canton-zug/matching-list?ipd=true',
    'https://www.homegate.ch/buy/apartment/canton-fribourg/matching-list?ipd=true',
    'https://www.homegate.ch/buy/apartment/canton-solothurn/matching-list?ipd=true',
    'https://www.homegate.ch/buy/apartment/canton-baselstadt/matching-list?ipd=true',
    'https://www.homegate.ch/buy/apartment/canton-baselland/matching-list?ipd=true',
    'https://www.homegate.ch/buy/apartment/canton-schaffhausen/matching-list?ipd=true',
    'https://www.homegate.ch/buy/apartment/canton-appenzellausserrhoden/matching-list?ipd=true',
    'https://www.homegate.ch/buy/apartment/canton-appenzellinnerrhoden/matching-list?ipd=true',
    'https://www.homegate.ch/buy/apartment/canton-stgallen/matching-list?ipd=true',
    'https://www.homegate.ch/buy/apartment/canton-graubuenden/matching-list?ipd=true',
    'https://www.homegate.ch/buy/apartment/canton-thurgau/matching-list?ipd=true',
    'https://www.homegate.ch/buy/apartment/canton-neuchatel/matching-list?ipd=true',
    'https://www.homegate.ch/buy/apartment/canton-geneva/matching-list?ipd=true',
    'https://www.homegate.ch/buy/apartment/canton-jura/matching-list?ipd=true',
    'https://www.homegate.ch/buy/apartment/canton-zurich/matching-list?ipd=true&ai=&aj=1400000',
    'https://www.homegate.ch/buy/apartment/canton-zurich/matching-list?ipd=true&ai=1400001&aj=',
    'https://www.homegate.ch/buy/apartment/canton-aargau/matching-list?ipd=true&ai=&aj=1400000',
    'https://www.homegate.ch/buy/apartment/canton-aargau/matching-list?ipd=true&ai=1400001&aj=',
    'https://www.homegate.ch/buy/apartment/canton-ticino/matching-list?ipd=true&ai=&aj=450000',
    'https://www.homegate.ch/buy/apartment/canton-ticino/matching-list?ipd=true&ai=450001&aj=600000',
    'https://www.homegate.ch/buy/apartment/canton-ticino/matching-list?ipd=true&ai=600001&aj=800000',
    'https://www.homegate.ch/buy/apartment/canton-ticino/matching-list?ipd=true&ai=800001&aj=1200000',
    'https://www.homegate.ch/buy/apartment/canton-ticino/matching-list?ipd=true&ai=1200001&aj=2000000',
    'https://www.homegate.ch/buy/apartment/canton-ticino/matching-list?ipd=true&ai=2000001&aj=',
    'https://www.homegate.ch/buy/apartment/canton-vaud/matching-list?ipd=true&ai=&aj=850000',
    'https://www.homegate.ch/buy/apartment/canton-vaud/matching-list?ipd=true&ai=850001&aj=1500000',
    'https://www.homegate.ch/buy/apartment/canton-vaud/matching-list?ipd=true&ai=1500001&aj=',
    'https://www.homegate.ch/buy/apartment/canton-valais/matching-list?ipd=true&ai=&aj=450000',
    'https://www.homegate.ch/buy/apartment/canton-valais/matching-list?ipd=true&ai=450001&aj=600000',
    'https://www.homegate.ch/buy/apartment/canton-valais/matching-list?ipd=true&ai=600001&aj=800000',
    'https://www.homegate.ch/buy/apartment/canton-valais/matching-list?ipd=true&ai=800001&aj='
]

scrape_links_rent = [
    'https://www.homegate.ch/rent/apartment/canton-lucerne/matching-list?ipd=true',
    'https://www.homegate.ch/rent/apartment/canton-uri/matching-list?ipd=true',
    'https://www.homegate.ch/rent/apartment/canton-schwyz/matching-list?ipd=true',
    'https://www.homegate.ch/rent/apartment/canton-obwalden/matching-list?ipd=true',
    'https://www.homegate.ch/rent/apartment/canton-nidwalden/matching-list?ipd=true',
    'https://www.homegate.ch/rent/apartment/canton-glarus/matching-list?ipd=true',
    'https://www.homegate.ch/rent/apartment/canton-zug/matching-list?ipd=true',
    'https://www.homegate.ch/rent/apartment/canton-fribourg/matching-list?ipd=true',
    'https://www.homegate.ch/rent/apartment/canton-baselstadt/matching-list?ipd=true',
    'https://www.homegate.ch/rent/apartment/canton-schaffhausen/matching-list?ipd=true',
    'https://www.homegate.ch/rent/apartment/canton-appenzellausserrhoden/matching-list?ipd=true',
    'https://www.homegate.ch/rent/apartment/canton-appenzellinnerrhoden/matching-list?ipd=true',
    'https://www.homegate.ch/rent/apartment/canton-graubuenden/matching-list?ipd=true',
    'https://www.homegate.ch/rent/apartment/canton-thurgau/matching-list?ipd=true',
    'https://www.homegate.ch/rent/apartment/canton-valais/matching-list?ipd=true',
    'https://www.homegate.ch/rent/apartment/canton-neuchatel/matching-list?ipd=true',
    'https://www.homegate.ch/rent/apartment/canton-geneva/matching-list?ipd=true',
    'https://www.homegate.ch/rent/apartment/canton-jura/matching-list?ipd=true',
    'https://www.homegate.ch/rent/apartment/canton-bern/matching-list?ipd=true&ag=&ah=1400',
    'https://www.homegate.ch/rent/apartment/canton-bern/matching-list?ipd=true&ag=1401&ah=1800',
    'https://www.homegate.ch/rent/apartment/canton-bern/matching-list?ipd=true&ag=1801&ah=',
    'https://www.homegate.ch/rent/apartment/canton-aargau/matching-list?ipd=true&ag=&ah=1700',
    'https://www.homegate.ch/rent/apartment/canton-aargau/matching-list?ipd=true&ag=1701&ah=',
    'https://www.homegate.ch/rent/apartment/canton-zurich/matching-list?ipd=true&ag=&ah=2100',
    'https://www.homegate.ch/rent/apartment/canton-zurich/matching-list?ipd=true&ag=2101&ah=3000',
    'https://www.homegate.ch/rent/apartment/canton-zurich/matching-list?ipd=true&ag=3001&ah=',
    'https://www.homegate.ch/rent/apartment/canton-solothurn/matching-list?ipd=true&ag=&ah=1600',
    'https://www.homegate.ch/rent/apartment/canton-solothurn/matching-list?ipd=true&ag=1601&ah=',
    'https://www.homegate.ch/rent/apartment/canton-baselland/matching-list?ipd=true&ag=&ah=1900',
    'https://www.homegate.ch/rent/apartment/canton-baselland/matching-list?ipd=true&ag=1901&ah=',
    'https://www.homegate.ch/rent/apartment/canton-stgallen/matching-list?ipd=true&ag=&ah=1500',
    'https://www.homegate.ch/rent/apartment/canton-stgallen/matching-list?ipd=true&ag=1501&ah=',
    'https://www.homegate.ch/rent/apartment/canton-ticino/matching-list?ipd=true&ag=&ah=1300',
    'https://www.homegate.ch/rent/apartment/canton-ticino/matching-list?ipd=true&ag=1301&ah=2000',
    'https://www.homegate.ch/rent/apartment/canton-ticino/matching-list?ipd=true&ag=2001&ah=',
    'https://www.homegate.ch/rent/apartment/canton-vaud/matching-list?ipd=true&ag=&ah=2000',
    'https://www.homegate.ch/rent/apartment/canton-vaud/matching-list?ipd=true&ag=2001&ah='
]

bounds_outliers = {
    'apartment_buy': {
        'living_space': (12, 250),
        'sqm_per_room': (7.5, 150),
        'price_sqm': (2500, 20000),
        'price': (50000, 3_000_000),
    },
    'house_buy': {
        'living_space': (20, 500),
        'sqm_per_room': (7.5, 150),
        'price_sqm': (1000, 20000),
        'price': (50000, 5_000_000),
    },
    'apartment_rent': {
        'living_space': (12, 200),
        'sqm_per_room': (7.5, 150),
        'price_sqm': (10, 50),
        'price': (400, 5000),
    },
    'house_rent': {
        'living_space': (20, 500),
        'sqm_per_room': (7.5, 150),
        'price_sqm': (0, 10_000_000),
        'price': (0, 10_000_000),
    },
}

living_space_ranges = {
    'apartment_buy': {
        'bins': [0, 40, 60, 80, 100, 150, 200, float('inf')],
        'labels': ['0-40', '41-60', '61-80', '81-100', '101-150', '151-200', '200+']
    },
    'house_buy': {
        'bins': [0, 40, 60, 80, 100, 150, 200, float('inf')],
        'labels': ['0-40', '41-60', '61-80', '81-100', '101-150', '151-200', '200+']
    },
    'apartment_rent': {
        'bins': [0, 40, 60, 80, 100, 150, 200, float('inf')],
        'labels': ['0-40', '41-60', '61-80', '81-100', '101-150', '151-200', '200+']
    },
    'house_rent': {
        'bins': [0, 40, 60, 80, 100, 150, 200, float('inf')],
        'labels': ['0-40', '41-60', '61-80', '81-100', '101-150', '151-200', '200+']
    }
}
