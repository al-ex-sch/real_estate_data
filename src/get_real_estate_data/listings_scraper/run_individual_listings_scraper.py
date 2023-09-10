##
import os

import pandas as pd
from dotenv import load_dotenv

import undetected_chromedriver as uc

from src.get_real_estate_data.listings_scraper.individual_listings_scraper import IndividualListingsScraper
from src.get_real_estate_data.shared.config import details_paths, path_images, paths_helper

load_dotenv()

file_path = os.getenv("file_path")

df_links = pd.read_csv(file_path, index_col=False)
df_links = df_links[49:51]

my_driver = uc.Chrome()


data_extractor = IndividualListingsScraper(
    driver=my_driver, elems_path=details_paths, imgs_path=path_images, helper_path=paths_helper,
)
ad_details_df = data_extractor.scrape_all_properties(df=df_links)
