##
import pandas as pd

from src.get_real_estate_data.d_nlp.text_processor import TextProcessor
from src.get_real_estate_data.d_nlp.topic_model_analyzer import TopicModelAnalyzer
from src.get_real_estate_data.d_nlp.word_2_vec import Word2VecProcessor


apt_buy = pd.read_csv(
    '/buy_less_words.csv'
)
apt_rent = pd.read_csv(
    '/rent_less_words.csv'
)


remove = [
    'floor', 'kitchen', 'live', 'space', 'bathroom', 'chf', 'contact', 'look', 'us', 'rent', 'toilet', 'forward',
    'look_forward', 'property', 'follow', 'interest', 'month', 'please', 'reach', 'use', 'room', 'contact_us',
    'appointment', 'also', 'date', 'rent_chf', 'view_date', 'available', 'chf_per', 'call', 'inquiry', 'chf_month',
    'write', 'space_chf', 'forward_contact', 'look_forward_contact', 'us_write', 'forward_inquiry',
    'look_forward_inquiry', 'please_contact', 'date_please', 'date_please_contact', 'use_contact_form', 'use_contact',
    'contact_form', 'please_contact_us', 'contact_us_write', '',
]


def nlp_pipe(df_buy, df_rent, remove_words):
    # DESCRIPTION PROCESSING -> text_translated_tokenized
    text_prep = TextProcessor(words_to_remove=remove_words)
    df_buy = text_prep.process_dataframe(df=df_buy, column_name='text_translated')
    df_rent = text_prep.process_dataframe(df=df_rent, column_name='text_translated')
    # EMBEDDINGS -> 100 feats
    word2vec_processor = Word2VecProcessor()
    word2vec_processor.train_word2vec_model(df_rent, df_buy)
    rent_with_word2vec = word2vec_processor.add_word2vec_features(df_rent)
    buy_with_word2vec = word2vec_processor.add_word2vec_features(df_buy)
    return rent_with_word2vec, buy_with_word2vec


rent_with_word2vec, buy_with_word2vec = nlp_pipe(apt_buy, apt_rent, remove)

# TODO: incorporate LDA -> dominant_topic feature
analyzer = TopicModelAnalyzer(apt_buy, 'text_translated_tokenized')
df = analyzer.analyze()
