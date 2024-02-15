##
import gensim
import pandas as pd
import numpy as np


class Word2VecProcessor:
    def __init__(self, vector_size=100, window=5, min_count=1, workers=4):
        self.vector_size = vector_size
        self.window = window
        self.min_count = min_count
        self.workers = workers
        self.model = None

    def train_word2vec_model(self, df1, df2):
        sentences = df1['text_translated_2'].tolist() + df2['text_translated_2'].tolist()
        self.model = gensim.models.Word2Vec(
            sentences=sentences,
            vector_size=self.vector_size,
            window=self.window,
            min_count=self.min_count,
            workers=self.workers,
        )

    @staticmethod
    def get_doc_embedding(words_list, model):
        embeddings = [model.wv[word] for word in words_list if word in model.wv]
        if len(embeddings) == 0:
            return np.zeros(model.vector_size)
        return np.mean(embeddings, axis=0)

    def word2vec_to_dataframe(self, words_list, index):
        vectors = [self.get_doc_embedding(words, self.model) for words in words_list]
        return pd.DataFrame(vectors, index=index)

    def add_word2vec_features(self, df):
        word2vec_df = self.word2vec_to_dataframe(df['text_translated_2'], df.index)
        word2vec_df.columns = [f'w2v_{i}' for i in range(word2vec_df.shape[1])]
        df_with_word2vec = df.merge(word2vec_df, left_index=True, right_index=True)
        return df_with_word2vec
