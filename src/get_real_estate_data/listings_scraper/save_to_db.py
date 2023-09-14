##
import os
from typing import Dict

import psycopg2 as ps
import pandas as pd
from dotenv import load_dotenv

from src.get_real_estate_data.listings_scraper.features_split import SplitFeatures


load_dotenv()

file_path = os.getenv("filepath")

host_name_ = os.getenv("host_name")
db_name_ = os.getenv("db_name")
port_ = 5432
username_ = os.getenv("db_username")
password_ = os.getenv("db_password")

data = pd.read_csv(file_path, index_col=False)

processor = SplitFeatures()
df = processor.process_data(df=data)


def connect_to_db(host_name, db_name, port, username, password):
    try:
        connection = ps.connect(host=host_name, dbname=db_name, port=port, user=username, password=password)
    except ps.OperationalError as e:
        raise e
    else:
        print('Connected.')
    return connection


def create_table(curr, table_name: str, cols_dict: Dict):
    columns_str = ', '.join(f"{col} {dtype}" for col, dtype in cols_dict.items())
    create_table_command = (
        f"""  
        CREATE TABLE IF NOT EXISTS {table_name} (  
            {columns_str}  
        )  
        """
    )

    curr.execute(create_table_command)


columns = {
    'link': 'VARCHAR(255)',
    'property_id': 'VARCHAR(255) PRIMARY KEY',
    'price': 'INTEGER NOT NULL',
    'page': 'INTEGER NOT NULL',
    'title': 'TEXT NOT NULL',
    'address': 'TEXT NOT NULL',
    'no_rooms': 'REAL',
    'living_area': 'INTEGER',
    'main_info': 'TEXT',
    'features_furnishings': 'TEXT',
    'advertiser': 'TEXT',
    'description': 'TEXT',
    'image_links': 'TEXT',
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
    'last_refurbishment': 'INTEGER',
    'year_built': 'INTEGER',
    'number_of_apartments': 'INTEGER',
    'number_of_floors': 'INTEGER',
    'land_area': 'TEXT',
    'volume': 'TEXT',
    'floor_space': 'TEXT',
    'room_height': 'TEXT'
}


conn = connect_to_db(host_name=host_name_, db_name=db_name_, port=port_, username=username_, password=password_)


##
curr = conn.cursor()
create_table(curr=curr, table_name='my_table', cols_dict=columns)
conn.commit()
