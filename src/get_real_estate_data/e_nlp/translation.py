##
import os

import pandas as pd
import openai
from dotenv import find_dotenv, load_dotenv


_ = load_dotenv(find_dotenv())
openai.api_key = os.environ['OPENAI_API_KEY']

df_apt_buy = pd.read_csv(
    'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/df_apt_buy_new.csv', index_col=0,
)
df_apt_rent = pd.read_csv(
    'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/df_apt_rent_new.csv', index_col=0,
)

df_apt_rent = df_apt_rent.rename(columns={'price': 'rent', 'price_sqm': 'rent_sqm'})

df_apt_rent = df_apt_rent[8:10]


class TextTranslator:
    def __init__(self, df, text_column='text', translated_column='text_translated'):
        self.df = df
        self.text_column = text_column
        self.translated_column = translated_column

    @staticmethod
    def translate_to_english(text):
        messages = [
            {"role": "system", "content": "You are a helpful assistant that translates text."},
            {"role": "user", "content": f"Translate the following text to English:\n\n{text}\n\nTranslation:"}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0,
        )
        translated_text = response.choices[0].message['content']
        return translated_text

    def translate_column(self):
        self.df[self.translated_column] = self.df[self.text_column].apply(self.translate_to_english)
        return self.df


translator = TextTranslator(df_apt_rent)
translated_df = translator.translate_column()
