##
import matplotlib.pyplot as plt
import seaborn as sns


class WordFrequencyAnalyzer:
    @staticmethod
    def count_words(tokenized_texts):
        word_counts = {}
        for tokens in tokenized_texts:
            for token in tokens:
                if token in word_counts:
                    word_counts[token] += 1
                else:
                    word_counts[token] = 1
        return word_counts

    def get_sorted_word_frequencies(self, df, column):
        tokenized_texts = df[column]
        word_frequencies = self.count_words(tokenized_texts)
        sorted_word_frequencies = {
            k: v for k, v in sorted(word_frequencies.items(), key=lambda item: item[1], reverse=True)
        }
        return sorted_word_frequencies

    @staticmethod
    def print_sorted_word_frequencies(sorted_word_frequencies):
        for word, count in sorted_word_frequencies.items():
            print(f'{word}: {count}')

    @staticmethod
    def plot_top_n_word_frequencies(sorted_word_frequencies, top_n_words=20):
        top_words = {k: sorted_word_frequencies[k] for k in list(sorted_word_frequencies)[:top_n_words]}

        plt.figure(figsize=(12, 8))
        sns.barplot(x=list(top_words.keys()), y=list(top_words.values()))
        plt.title(f'Top {top_n_words} Word Frequencies')
        plt.xlabel('Words')
        plt.ylabel('Frequencies')
        plt.xticks(rotation=45)
        plt.show()
