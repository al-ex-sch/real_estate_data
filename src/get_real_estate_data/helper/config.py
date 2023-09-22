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


details_paths = {
    'title': 'h1.ListingTitle_spotlightTitle_ENVSi',
    'address': 'address.AddressDetails_address_i3koO',
    'no_rooms': 'div.SpotlightAttributesNumberOfRooms_value_TUMrd',
    'living_area': 'div.SpotlightAttributesLivingSpace_value_OiuVM',
    'main_info': 'div.CoreAttributes_coreAttributes_e2NAm',
    'features_furnishings': 'ul.FeaturesFurnishings_list_S54KV',
    'advertiser': 'p.ListerContactPhone_person_hZLKb',
    'description': 'div.Description_descriptionBody_AYyuy',
    'image_links': 'li.glide__slide img',
}

path_images = {
    'load_images_button': 'button.HgArrowButton_arrowButton_yXU5A',
    'image_count_1': '//*[@id="app"]/main/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/div[1]/div/div/div[2]/button/span',
    'image_count_2': '//*[@id="app"]/main/div/div[2]/div[1]/div[2]/div[1]/div[2]/div/div[1]/div/div/div[2]/button/span',
}


paths_helper = {
    'cookies': '//*[@id="onetrust-accept-btn-handler"]',
    'hover': 'a:nth-child(7)',
    'detect_unavailable_prop': 'div.SpotlightAttributesPrice_value_TqKGz',
}

cols_dict = {
    'property_id': 'VARCHAR(255) NOT NULL',
    'price': 'INTEGER',
    'address': 'TEXT',
    'rooms': 'REAL',
    'living_space': 'INTEGER',
    'text': 'TEXT',
    'image_url': 'TEXT',
    'link': 'TEXT',
    'page': 'INTEGER',

    'first_date_on_stock': 'DATE',
    'first_price': 'INTEGER',
    'stock': 'BOOLEAN',
    'sold': 'BOOLEAN',
    'new': 'BOOLEAN',
    'drops': 'INTEGER',
    'increases': 'INTEGER',
    'stock_date': 'DATE',
    'last_date_on_stock': 'DATE',
    'last_price': 'INTEGER',
    'dis_sold': 'INTEGER',
    'dis_stock': 'INTEGER',
}

cols_dict_details = {
    'property_id': 'VARCHAR(255) NOT NULL',
    'price': 'INTEGER',
    'page': 'INTEGER',
    'title': 'TEXT',
    'address': 'TEXT',
    'no_rooms': 'REAL',
    'living_area': 'INTEGER',
    'main_info': 'TEXT',
    'features_furnishings': 'TEXT',
    'advertiser': 'TEXT',
    'description': 'TEXT',
    'image_links': 'TEXT',
    'link': 'TEXT',

    'first_date_on_stock': 'DATE',
    'first_price': 'INTEGER',
    'stock': 'BOOLEAN',
    'sold': 'BOOLEAN',
    'new': 'BOOLEAN',
    'drops': 'INTEGER',
    'increases': 'INTEGER',
    'stock_date': 'DATE',
    'last_date_on_stock': 'DATE',
    'last_price': 'INTEGER',
    'dis_sold': 'INTEGER',
    'dis_stock': 'INTEGER',

    'balcony_terrace': 'BOOLEAN',
    'cable_tv': 'BOOLEAN',
    'child_friendly': 'BOOLEAN',
    'connected_land_for_building': 'BOOLEAN',
    'elevator': 'BOOLEAN',
    'fireplace': 'BOOLEAN',
    'garage': 'BOOLEAN',
    'mid_terrace_house': 'BOOLEAN',
    'minergie_certified': 'BOOLEAN',
    'minergie_construction': 'BOOLEAN',
    'new_building': 'BOOLEAN',
    'old_building': 'BOOLEAN',
    'parking_space': 'BOOLEAN',
    'pets_allowed': 'BOOLEAN',
    'quiet_neighborhood': 'BOOLEAN',
    'raised_ground_floor': 'BOOLEAN',
    'smoking_permitted': 'BOOLEAN',
    'swimming_pool': 'BOOLEAN',
    'view': 'BOOLEAN',
    'washing_machine': 'BOOLEAN',
    'wheelchair_access': 'BOOLEAN',

    'type': 'VARCHAR(255)',
    'no_of_rooms': 'REAL',
    'floor': 'TEXT',
    'surface_living': 'TEXT',
    'last_refurbishment': 'TEXT',
    'year_built': 'INTEGER',
    'number_of_apartments': 'INTEGER',
    'number_of_floors': 'INTEGER',
    'land_area': 'TEXT',
    'volume': 'TEXT',
    'floor_space': 'TEXT',
    'room_height': 'TEXT'
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

scrape_links = [
    # 'https://www.homegate.ch/buy/apartment/canton-bern/matching-list?ipd=true',
    # 'https://www.homegate.ch/buy/apartment/canton-lucerne/matching-list?ipd=true',
    # 'https://www.homegate.ch/buy/apartment/canton-uri/matching-list?ipd=true',
    # 'https://www.homegate.ch/buy/apartment/canton-schwyz/matching-list?ipd=true',
    # 'https://www.homegate.ch/buy/apartment/canton-obwalden/matching-list?ipd=true',
    # 'https://www.homegate.ch/buy/apartment/canton-nidwalden/matching-list?ipd=true',
    # 'https://www.homegate.ch/buy/apartment/canton-glarus/matching-list?ipd=true',
    # 'https://www.homegate.ch/buy/apartment/canton-zug/matching-list?ipd=true',
    # 'https://www.homegate.ch/buy/apartment/canton-fribourg/matching-list?ipd=true',
    # 'https://www.homegate.ch/buy/apartment/canton-solothurn/matching-list?ipd=true',
    # 'https://www.homegate.ch/buy/apartment/canton-baselstadt/matching-list?ipd=true',
    # 'https://www.homegate.ch/buy/apartment/canton-baselland/matching-list?ipd=true',
    # 'https://www.homegate.ch/buy/apartment/canton-schaffhausen/matching-list?ipd=true',
    # 'https://www.homegate.ch/buy/apartment/canton-appenzellausserrhoden/matching-list?ipd=true',
    # 'https://www.homegate.ch/buy/apartment/canton-appenzellinnerrhoden/matching-list?ipd=true',
    # 'https://www.homegate.ch/buy/apartment/canton-stgallen/matching-list?ipd=true',
    # 'https://www.homegate.ch/buy/apartment/canton-graubuenden/matching-list?ipd=true',
    # 'https://www.homegate.ch/buy/apartment/canton-thurgau/matching-list?ipd=true',
    # 'https://www.homegate.ch/buy/apartment/canton-neuchatel/matching-list?ipd=true',
    # 'https://www.homegate.ch/buy/apartment/canton-geneva/matching-list?ipd=true',
    # 'https://www.homegate.ch/buy/apartment/canton-jura/matching-list?ipd=true',
    # 'https://www.homegate.ch/buy/apartment/canton-zurich/matching-list?ipd=true&ai=&aj=1400000',
    # 'https://www.homegate.ch/buy/apartment/canton-zurich/matching-list?ipd=true&ai=1400001&aj=',
    # 'https://www.homegate.ch/buy/apartment/canton-aargau/matching-list?ipd=true&ai=&aj=1400000',
    # 'https://www.homegate.ch/buy/apartment/canton-aargau/matching-list?ipd=true&ai=1400001&aj=',
    # 'https://www.homegate.ch/buy/apartment/canton-ticino/matching-list?ipd=true&ai=&aj=450000',
    # 'https://www.homegate.ch/buy/apartment/canton-ticino/matching-list?ipd=true&ai=450001&aj=600000',
    # 'https://www.homegate.ch/buy/apartment/canton-ticino/matching-list?ipd=true&ai=600001&aj=800000',
    # 'https://www.homegate.ch/buy/apartment/canton-ticino/matching-list?ipd=true&ai=800001&aj=1200000',
    # 'https://www.homegate.ch/buy/apartment/canton-ticino/matching-list?ipd=true&ai=1200001&aj=2000000',
    'https://www.homegate.ch/buy/apartment/canton-ticino/matching-list?ipd=true&ai=2000001&aj=',
    'https://www.homegate.ch/buy/apartment/canton-vaud/matching-list?ipd=true&ai=&aj=850000',
    'https://www.homegate.ch/buy/apartment/canton-vaud/matching-list?ipd=true&ai=850001&aj=1500000',
    'https://www.homegate.ch/buy/apartment/canton-vaud/matching-list?ipd=true&ai=1500001&aj=',
    'https://www.homegate.ch/buy/apartment/canton-valais/matching-list?ipd=true&ai=&aj=450000',
    'https://www.homegate.ch/buy/apartment/canton-valais/matching-list?ipd=true&ai=450001&aj=600000',
    'https://www.homegate.ch/buy/apartment/canton-valais/matching-list?ipd=true&ai=600001&aj=800000',
    'https://www.homegate.ch/buy/apartment/canton-valais/matching-list?ipd=true&ai=800001&aj='
]
