##
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.util import ngrams
import string
import re
import contractions
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


class TextProcessor:
    def __init__(self, words_to_remove):
        self.words_to_remove = words_to_remove
        self.wordnet_lemmatizer = WordNetLemmatizer()
        self.stopword = stopwords.words('english')

    def _remove_specified_words(self, tokens):
        """
        Remove specified words from the list of tokens.

        :param tokens: List of tokens.
        :return: List of tokens with specified words removed.
        """
        cleaned_tokens = [token for token in tokens if token not in self.words_to_remove]
        return cleaned_tokens

    @staticmethod
    def _remove_links(text):
        return re.sub(r'http\S+|www\S+|https\S+', '', text)

    @staticmethod
    def remove_punctuation(text):
        no_punct = [w for w in text if w not in string.punctuation]
        words_wo_punct = ''.join(no_punct)
        return words_wo_punct

    @staticmethod
    def _tokenize_text(text):
        return word_tokenize(text)

    @staticmethod
    def _lower_case(text):
        return [w.lower() for w in text]

    def _remove_stopwords(self, text):
        custom_words = ['apartment', 'room', 'rent', '•', '"', "'"]
        self.stopword.extend(custom_words)
        return [w for w in text if w not in self.stopword]

    def _lemmatize_text(self, text):
        return [self.wordnet_lemmatizer.lemmatize(w, pos="v") for w in text]

    @staticmethod
    def _generate_ngrams(tokens, n=2):
        ngram_tuples = list(ngrams(tokens, n))
        ngram_strings = ['_'.join(words) for words in ngram_tuples]
        return ngram_strings

    @staticmethod
    def _replace_punctuation_with_space(text):
        text = text.replace("•", "").replace("\"", "")
        punctuation = ''.join([char for char in string.punctuation if char != "'"])
        text = re.sub(r'([' + re.escape(punctuation) + r'])(\S)', r'\1 \2', text)
        text = ''.join([char if char not in punctuation else '' for char in text])
        text = re.sub(' +', ' ', text)
        return text

    @staticmethod
    def _expand_contractions(text):
        return contractions.fix(text)

    @staticmethod
    def _remove_numbers(text):
        return ''.join([char for char in text if not char.isdigit()])

    def _preprocess_text(self, text):
        text = self._remove_links(text)
        text = self._replace_punctuation_with_space(text)
        text = self._expand_contractions(text)
        text = self._remove_numbers(text)
        tokens = self._tokenize_text(text)
        tokens = self._lower_case(tokens)
        tokens = self._remove_stopwords(tokens)
        tokens = self._lemmatize_text(tokens)
        bigrams = self._generate_ngrams(tokens, 2)
        trigrams = self._generate_ngrams(tokens, 3)
        tokens = tokens + bigrams + trigrams
        tokens = self._remove_specified_words(tokens=tokens)
        return tokens

    def process_dataframe(self, df, column_name):
        """
        Process the dataframe with given column and add a new column with transformed tokens.

        :param df: DataFrame to process.
        :param column_name: Column name containing text to process.
        :return: DataFrame with a new column named 'text_transformed' containing transformed tokens.
        """
        df[column_name + '_tokenized'] = df[column_name].fillna('')
        for index, row in df.iterrows():
            print(f"Processing row {index}")
            df.at[index, column_name + '_tokenized'] = self._preprocess_text(row[column_name])
        return df
