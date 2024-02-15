##
import pandas as pd

from src.get_real_estate_data.d_nlp.topic_model_analyzer import TopicModelAnalyzer
from src.get_real_estate_data.d_nlp.word_frequency_analyzer import WordFrequencyAnalyzer
import ast


buy = pd.read_csv(
    '/tokenized_buy.csv'
)
rent = pd.read_csv(
    '/tokenized_rent.csv'
)

# TODO: omylem jsem prepsala text translated - vratit


analyzer = WordFrequencyAnalyzer()
sorted_word_frequencies_rent = analyzer.get_sorted_word_frequencies(rent, 'text_translated')
analyzer.print_sorted_word_frequencies(sorted_word_frequencies_rent)
analyzer.plot_top_n_word_frequencies(sorted_word_frequencies_rent, top_n_words=20)


analyzer = WordFrequencyAnalyzer()
sorted_word_frequencies_buy = analyzer.get_sorted_word_frequencies(buy, 'text_translated')
analyzer.print_sorted_word_frequencies(sorted_word_frequencies_buy)
analyzer.plot_top_n_word_frequencies(sorted_word_frequencies_buy, top_n_words=20)


def get_common_words(dict1, dict2):
    common_words = {
        word: (dict1[word], dict2[word])
        for word in dict1 if word in dict2
    }
    return common_words


common_words = get_common_words(sorted_word_frequencies_rent, sorted_word_frequencies_buy)


common_words_df = pd.DataFrame.from_dict(common_words, orient='index', columns=['rent_frequency', 'buy_frequency']).reset_index()

##

threshold = 10
filtered_common_words_df = common_words_df[
    (common_words_df['rent_frequency'] > threshold) & (common_words_df['buy_frequency'] > threshold)]

words_to_remove = ['']
filtered_common_words_df = filtered_common_words_df[~filtered_common_words_df['index'].isin(words_to_remove)]

filtered_words = set(filtered_common_words_df['index'].tolist())


def filter_words(text_translated):
    return [word for word in text_translated if word in filtered_words]


rent['text_translated'] = rent['text_translated'].apply(ast.literal_eval)
buy['text_translated'] = buy['text_translated'].apply(ast.literal_eval)

rent['text_translated_2'] = rent['text_translated'].apply(filter_words)
buy['text_translated_2'] = buy['text_translated'].apply(filter_words)

##

rent.to_csv('rent_less_words.csv')
buy.to_csv('buy_less_words.csv')


##

filtered_common_words_df.to_excel('words.xlsx')


##

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


def join_words(words_list):
    return ' '.join(words_list)


rent['text_translated_2_joined'] = rent['text_translated_2'].apply(join_words)
buy['text_translated_2_joined'] = buy['text_translated_2'].apply(join_words)

bow_vectorizer = CountVectorizer()
rent_bow = bow_vectorizer.fit_transform(rent['text_translated_2_joined'])
buy_bow = bow_vectorizer.transform(buy['text_translated_2_joined'])

tfidf_vectorizer = TfidfVectorizer()
rent_tfidf = tfidf_vectorizer.fit_transform(rent['text_translated_2_joined'])
buy_tfidf = tfidf_vectorizer.transform(buy['text_translated_2_joined'])


##

import gensim
import numpy as np


word2vec_model = gensim.models.Word2Vec(
    sentences=rent['text_translated_2'].tolist() + buy['text_translated_2'].tolist(), vector_size=100, window=5,
    min_count=1, workers=4)


def get_doc_embedding(words_list, model):
    embeddings = [model.wv[word] for word in words_list if word in model.wv]
    if len(embeddings) == 0:
        return np.zeros(model.vector_size)
    return np.mean(embeddings, axis=0)


rent_word2vec = rent['text_translated_2'].apply(lambda x: get_doc_embedding(x, word2vec_model))
buy_word2vec = buy['text_translated_2'].apply(lambda x: get_doc_embedding(x, word2vec_model))

rent_word2vec = np.vstack(rent_word2vec.values)
buy_word2vec = np.vstack(buy_word2vec.values)

##

def word2vec_to_dataframe(words_list, model, index):
    vectors = [get_doc_embedding(words, model) for words in words_list]
    return pd.DataFrame(vectors, index=index)


rent_word2vec_df = word2vec_to_dataframe(rent['text_translated_2'], word2vec_model, rent.index)

rent_word2vec_df.columns = [f'w2v_{i}' for i in range(rent_word2vec_df.shape[1])]

rent_with_word2vec = rent.merge(rent_word2vec_df, left_index=True, right_index=True)


##

import gensim
import numpy as np

word2vec_model = gensim.models.Word2Vec(
    sentences=rent['text_translated_2'].tolist() + buy['text_translated_2'].tolist(), vector_size=100, window=5,
    min_count=1, workers=4)

common_words = {'parquet', 'transportation', 'beautiful_view'}


def average_word2vec(words_list, model, common_words):
    embeddings = [model.wv[word] for word in words_list if word in model.wv and word in common_words]
    if len(embeddings) == 0:
        return np.zeros(model.vector_size)
    return np.mean(embeddings, axis=0)


rent['avg_word2vec'] = rent['text_translated_2'].apply(lambda x: average_word2vec(x, word2vec_model, common_words))
buy['avg_word2vec'] = buy['text_translated_2'].apply(lambda x: average_word2vec(x, word2vec_model, common_words))
