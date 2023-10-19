##
import psutil
from typing import List

import undetected_chromedriver as uc

from src.get_real_estate_data.b_links_scraper.property_links_scraper import PropertyLinksScraper
from src.get_real_estate_data.a_helper.config import links_paths, paths_helper, scrape_links  # scrape_links_rent


def kill_chrome_processes():
    for process in psutil.process_iter():
        try:
            if "chrome" in process.name().lower():
                process.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


def scrape_all_cantons_properties(links_to_scrape: List) -> None:
    canton_counters = {}
    for link in links_to_scrape:
        my_driver = uc.Chrome()
        canton_name = link.split("/buy/apartment/")[1].split("/matching-list")[0]
        if canton_name not in canton_counters:
            canton_counters[canton_name] = 0
        else:
            canton_counters[canton_name] += 1
        scraper = PropertyLinksScraper(
            driver=my_driver,
            page_url=link,
            elems_path=links_paths,
            helper_path=paths_helper,
            canton_name=canton_name,
            canton_counter=canton_counters[canton_name],
        )
        scraper.scrape_data()

        kill_chrome_processes()


scrape_all_cantons_properties(scrape_links)
