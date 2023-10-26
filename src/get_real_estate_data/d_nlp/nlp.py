##
import pandas as pd

from src.get_real_estate_data.d_nlp.text_processor import TextProcessor
from src.get_real_estate_data.d_nlp.topic_model_analyzer import TopicModelAnalyzer
from src.get_real_estate_data.d_nlp.word_frequency_analyzer import WordFrequencyAnalyzer


df1 = pd.read_csv('nlp.csv')

##

remove = [
    'floor', 'kitchen', 'live', 'space', 'bathroom', 'chf', 'contact', 'look', 'us', 'rent', 'toilet', 'forward',
    'look_forward', 'property', 'follow', 'interest', 'month', 'please', 'reach', 'use', 'room', 'contact_us',
    'appointment', 'also', 'date', 'rent_chf', 'view_date', 'available', 'chf_per', 'call', 'inquiry', 'chf_month',
    'write', 'space_chf', 'forward_contact', 'look_forward_contact', 'us_write', 'forward_inquiry',
    'look_forward_inquiry', 'please_contact', 'date_please', 'date_please_contact', 'use_contact_form', 'use_contact',
    'contact_form', 'please_contact_us', 'contact_us_write', '',
]
text_prep = TextProcessor(words_to_remove=remove)
df2 = text_prep.process_dataframe(df=df1, column_name='translated_text')


##

analyzer = WordFrequencyAnalyzer()
sorted_word_frequencies = analyzer.get_sorted_word_frequencies(df2, 'text_transformed')
analyzer.print_sorted_word_frequencies(sorted_word_frequencies)
analyzer.plot_top_n_word_frequencies(sorted_word_frequencies, top_n_words=20)

##

# add
analyzer = TopicModelAnalyzer(df2, 'text_transformed')
df3 = analyzer.analyze()


##
df3.to_csv('nlp2.csv')


##

from sklearn.feature_extraction.text import TfidfVectorizer

documents = [
    'quiet area, bright, close to shop',
    'spacious apartment, close to park, quiet',
    'modern design, bright, close to city center',
    'close to school, park nearby, quiet area'
]

# TF-IDF

# Create a TfidfVectorizer instance
vectorizer = TfidfVectorizer(stop_words='english')

# Fit and transform the documents into a TF-IDF matrix
tfidf_matrix = vectorizer.fit_transform(documents)

# Feature names (words)
feature_names = vectorizer.get_feature_names_out()

# Print the TF-IDF matrix
for doc_idx, tfidf_vector in enumerate(tfidf_matrix.toarray()):
    print(f"Document {doc_idx + 1}:")
    for word_idx, score in enumerate(tfidf_vector):
        if score > 0:
            print(f"{feature_names[word_idx]}: {score:.4f}")
    print()

# create vectors
