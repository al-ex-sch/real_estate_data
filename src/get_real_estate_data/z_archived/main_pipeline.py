##
import os
from typing import Dict

import pandas as pd

import undetected_chromedriver as uc
from dotenv import load_dotenv

from src.get_real_estate_data.c_preprocessing.property_tracker import PropertyTracker
from src.get_real_estate_data.a_helper.config import links_paths, paths_helper, path_images, details_paths, cols_dict
from src.get_real_estate_data.b_links_scraper.property_links_scraper import PropertyLinksScraper
from src.get_real_estate_data.z_archived.individual_listings_scraper import IndividualListingsScraper
from src.get_real_estate_data.g_save_to_db.process_before_saving_to_db import ProcessBeforeSavingToDb
from src.get_real_estate_data.g_save_to_db.save_to_db import SaveToDb

pd.set_option("mode.chained_assignment", None)

load_dotenv()
my_url_ = os.getenv("my_url")
table_name_ = 'test3'


class MainPipeline:

    def __init__(self, my_url: str, table_name: str, cols_n_types: Dict):
        self.my_url = my_url
        self.table_name = table_name
        self.cols_n_types = cols_n_types

        self.table_name2 = 'test333'
        self.host_name = os.getenv("host_name")
        self.db_name = os.getenv("db_name")
        self.port = 5432
        self.username = os.getenv("db_username")
        self.password = os.getenv("db_password")

    def _scrape_today_links(self):
        my_driver = uc.Chrome()
        property_links_scraper = PropertyLinksScraper(
            driver=my_driver, page_url=self.my_url, elems_path=links_paths, helper_path=paths_helper
        )
        return property_links_scraper.scrape_data()

    def _create_connection(self):
        dbutils = SaveToDb()
        conn = dbutils.connect_to_db(
            host_name=self.host_name,
            db_name=self.db_name,
            port=self.port,
            username=self.username,
            password=self.password,
        )
        return conn, dbutils

    def _get_yesterday_df(self):
        conn, _ = self._create_connection()
        query = f"""  
            SELECT * FROM {self.table_name2}  
            WHERE stock_date = (  
                SELECT MAX(stock_date) FROM {self.table_name2}  
            )  
        """
        yesterday_df = pd.read_sql_query(query, conn)
        conn.close()
        return yesterday_df

    @staticmethod
    def _track_properties(yesterday_df, today_df):
        property_tracker = PropertyTracker()
        return property_tracker.perform_property_tracking(yesterday=yesterday_df, today=today_df)

    def _save_data_to_db(self, df):
        conn, dbutils = self._create_connection()
        preprocess = ProcessBeforeSavingToDb()
        preprocessed_df = preprocess.perform_preprocessing(df=df, cols_n_datatypes=self.cols_n_types)
        dbutils.insert_df_to_db(df=preprocessed_df, table_name=self.table_name, conn=conn)
        conn.close()

    @staticmethod
    def _scrape_individual_listings(new_df):
        driver_listings = uc.Chrome()
        data_extractor = IndividualListingsScraper(
            driver=driver_listings, elems_path=details_paths, imgs_path=path_images, helper_path=paths_helper,
        )
        return data_extractor.scrape_all_properties(df=new_df)

    def _create_table(self):
        conn, dbutils = self._create_connection()
        dbutils.create_table(conn=conn, table_name=self.table_name, cols_dict=self.cols_n_types)
        conn.close()

    def run_pipeline(self):
        today_df = self._scrape_today_links()
        yesterday_df = self._get_yesterday_df()
        stock_df, new_df, sold_df = self._track_properties(yesterday_df, today_df)

        self._create_table()

        new_details_df = self._scrape_individual_listings(new_df)

        for df in [stock_df, sold_df, new_details_df]:
            self._save_data_to_db(df)


main_pipe = MainPipeline(table_name=table_name_, cols_n_types=cols_dict, my_url=my_url_)
main_pipe.run_pipeline()
