##
import os

from dotenv import load_dotenv
import undetected_chromedriver as uc

from src.get_real_estate_data.links_scraper.property_links_scraper import PropertyLinksScraper
from src.get_real_estate_data.shared.config import links_paths, paths_helper

load_dotenv()

my_url = os.getenv("my_url")

my_driver = uc.Chrome()

scraper = PropertyLinksScraper(driver=my_driver, page_url=my_url, elems_path=links_paths, helper_path=paths_helper)
scraper.scrape_data()
