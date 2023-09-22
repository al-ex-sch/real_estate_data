##
from typing import Dict

import psycopg2 as ps
from psycopg2 import connect
import pandas as pd


class DbUtils:
    @staticmethod
    def connect_to_db(host_name, db_name, port, username, password) -> connect:
        try:
            connection = ps.connect(host=host_name, dbname=db_name, port=port, user=username, password=password)
        except ps.OperationalError as e:
            raise e
        else:
            print('Connected.')
        return connection

    @staticmethod
    def create_table(table_name: str, cols_dict: Dict, conn: connect):
        curr = conn.cursor()
        columns_str = ', '.join(f"{col} {dtype}" for col, dtype in cols_dict.items())
        create_table_command = (
            f"""    
            CREATE TABLE IF NOT EXISTS {table_name} (    
                {columns_str}    
            )    
            """
        )

        curr.execute(create_table_command)
        conn.commit()

    @staticmethod
    def insert_df_to_db(df: pd.DataFrame, table_name: str, conn: connect):
        """
        Insert a DataFrame into a database table.

        :param df: The DataFrame to be inserted.
        :param table_name: The name of the database table.
        :param conn: The connection to the database.
        """
        records = df.to_dict(orient='records')
        columns = list(df.columns)
        insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"

        with conn.cursor() as cursor:
            for record in records:
                print("Insert query:", insert_query)
                print("Values:", list(record.values()))
                cursor.execute(insert_query, list(record.values()))

        conn.commit()

    @staticmethod
    def replace_data_in_table(df: pd.DataFrame, table_name: str, conn: connect, unique_column: str = 'property_id'):
        """
        Replace the data in a database table with new data from a DataFrame.

        :param df: The DataFrame containing the new data.
        :param table_name: The name of the database table.
        :param conn: The connection to the database.
        :param unique_column: The column with a unique constraint (primary key or unique index) in the table.
        """

        records = df.to_dict(orient='records')
        columns = list(df.columns)
        insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"
        conflict_update_clause = f" ON CONFLICT ({unique_column}) " \
                                 f"DO UPDATE SET {', '.join([f'{col}=EXCLUDED.{col}' for col in columns])}"

        upsert_query = insert_query + conflict_update_clause

        with conn.cursor() as cursor:
            for record in records:
                cursor.execute(upsert_query, list(record.values()))

        conn.commit()
