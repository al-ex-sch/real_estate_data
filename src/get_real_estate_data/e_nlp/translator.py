##
import pandas as pd
from googletrans import Translator


df_apt_buy = pd.read_csv(
    'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/df_apt_buy_new.csv', index_col=0,
)
df_apt_rent = pd.read_csv(
    'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/df_apt_rent_new.csv', index_col=0,
)


class TextTranslator:
    def __init__(self, df, text_column='text', translated_column='text_translated'):
        self.df = df
        self.text_column = text_column
        self.translated_column = translated_column
        self.translator = Translator()

    def translate_to_english(self, text):
        try:
            translated_text = self.translator.translate(text, dest='en').text
            return translated_text
        except Exception as e:
            print(f"Error occurred during translation: {e}")
            return None

    def translate_column(self):
        for index, row in self.df.iterrows():
            print(f"Translating row {index}")
            translated_text = self.translate_to_english(row[self.text_column])
            if translated_text is not None:
                self.df.at[index, self.translated_column] = translated_text
                self.df.to_csv('translated_df_temp.csv', index=False)
                print(f"Successfully translated and saved row {index}")
            else:
                print(f"Skipping record at index {index}")
        return self.df


translator = TextTranslator(df_apt_rent)
translated_df = translator.translate_column()
translated_df.to_csv('translated_rent_df.csv', index=False)
