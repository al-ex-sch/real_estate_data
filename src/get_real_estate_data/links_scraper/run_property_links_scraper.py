##
import psutil
from typing import List

import undetected_chromedriver as uc

from src.get_real_estate_data.links_scraper.property_links_scraper import PropertyLinksScraper
from src.get_real_estate_data.helper.config import links_paths, paths_helper, scrape_links


def kill_chrome_processes():
    for process in psutil.process_iter():
        try:
            if "chrome" in process.name().lower():
                process.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


def scrape_all_cantons_properties(links_to_scrape: List) -> None:
    for link in links_to_scrape:
        my_driver = uc.Chrome()
        canton_name = link.split("/buy/apartment/")[1].split("/matching-list")[0]
        scraper = PropertyLinksScraper(
            driver=my_driver,
            page_url=link,
            elems_path=links_paths,
            helper_path=paths_helper,
            canton_name=canton_name,
        )
        scraper.scrape_data()

        kill_chrome_processes()


scrape_all_cantons_properties(scrape_links)
