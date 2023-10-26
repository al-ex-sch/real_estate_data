##
import seaborn as sns
import matplotlib.pyplot as plt
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from sklearn.manifold import TSNE
import numpy as np


class TopicModelAnalyzer:
    def __init__(self, df, column):
        self.df = df
        self.column = column
        self.dictionary, self.corpus = self.create_dictionary_and_corpus()
        self.lda_model = None
        self.num_topics = None

    def create_dictionary_and_corpus(self):
        tokenized_texts = self.df[self.column]
        dictionary = corpora.Dictionary(tokenized_texts)
        corpus = [dictionary.doc2bow(text) for text in tokenized_texts]
        return dictionary, corpus

    def train_lda_model(self, num_topics=4, passes=15):
        self.num_topics = num_topics
        self.lda_model = LdaModel(self.corpus, num_topics=num_topics, id2word=self.dictionary, passes=passes)

    def print_top_words_for_topics(self, num_words=20):
        if not self.lda_model:
            print("Please train the LDA model before printing topics.")
            return

        for idx, topic in self.lda_model.print_topics(-1, num_words=num_words):
            print(f'Topic {idx + 1}: {topic}\n')

    def plot_top_words_seaborn(self, num_words=20):
        if not self.lda_model:
            print("Please train the LDA model before plotting top words.")
            return

        for topic_id in range(self.num_topics):
            top_words = self.lda_model.show_topic(topic_id, num_words)
            words, weights = zip(*top_words)

            plt.figure(figsize=(12, 4))
            sns.barplot(x=list(words), y=list(weights))
            plt.title(f'Topic {topic_id + 1}')
            plt.xlabel('Words')
            plt.ylabel('Weights')
            plt.show()

    def get_dominant_topic(self, doc_bow):
        topic_scores = self.lda_model[doc_bow]
        dominant_topic = sorted(topic_scores, key=lambda x: x[1], reverse=True)[0][0]
        return dominant_topic

    def assign_dominant_topic(self):
        self.df['dominant_topic'] = self.df[self.column].apply(
            lambda x: self.get_dominant_topic(self.dictionary.doc2bow(x))
        )

    def get_topic_proportions(self, doc_bow):
        topic_scores = self.lda_model[doc_bow]
        proportions = np.zeros(self.num_topics)

        for topic, score in topic_scores:
            proportions[topic] = score

        return proportions

    def assign_topic_proportions(self):
        self.df['topic_proportions'] = self.df[self.column].apply(
            lambda x: self.get_topic_proportions(self.dictionary.doc2bow(x))
        )

    def plot_tsne(self):
        tsne_model = TSNE(n_components=2, random_state=42)
        tsne_coordinates = tsne_model.fit_transform(np.array(list(self.df['topic_proportions'])))

        self.df['tsne_x'] = tsne_coordinates[:, 0]
        self.df['tsne_y'] = tsne_coordinates[:, 1]

        plt.figure(figsize=(12, 8))
        sns.scatterplot(x='tsne_x', y='tsne_y', hue='dominant_topic', palette='deep', data=self.df)
        plt.title('Documents in Different Quadrants')
        plt.xlabel('t-SNE Dimension 1')
        plt.ylabel('t-SNE Dimension 2')
        plt.legend(title='Dominant Topic')
        plt.show()

    def analyze(self, num_topics=4, passes=15, num_words=20):
        self.train_lda_model(num_topics, passes)
        self.print_top_words_for_topics(num_words)
        self.assign_dominant_topic()
        self.plot_top_words_seaborn(num_words)
        self.assign_topic_proportions()
        self.plot_tsne()
        return self.df
