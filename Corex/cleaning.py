import pandas as pd
import unicodedata
import re
import html
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem.snowball import SnowballStemmer
import gensim
from gensim.models import Phrases
import spacy
import os

nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])


# region Import Data
def read_in_chatlogs(path, column_name, max_chats):
    # Load in the data
    chats = pd.read_csv(path, nrows=max_chats) \
        .dropna(subset=[column_name]) \
        .reset_index(drop=True)[column_name]

    return chats


# Code is from unsupervised-clustering preprocessing.py
def initial_clean_chatlogs(chats, no_numbers=True):
    # Convert HTML versions of characters to their normal version
    chatlogs_html_cleaned = [html.unescape(x) for x in chats]

    # Replace some weird characters with spaces and remove numbers if requested
    r_query = r'[^a-zA-Z +\']' if no_numbers else r'[^a-zA-Z0-9 +\']'
    chatlogs_alnum_only = [re.sub(r_query, '', x.replace('\n', ' ').replace(':', ' ').replace(',', ' ')
                                  .replace('.', ' ')) for x in chatlogs_html_cleaned]

    # Strip whitespace, lower the case, and remove double spaces with regex
    chatlogs_cleaned = [re.sub('\\s+', ' ', x).strip().lower() for x in chatlogs_alnum_only]

    return chatlogs_cleaned


# endregion


# region Stopword Removal

def removestop(text, all_stops):
    return ' '.join([word for word in text.split(' ') if word not in all_stops])


def remove_accents(input_str):
    return unicodedata.normalize('NFKD', input_str).encode('ASCII', 'ignore')


def remove_all_stopwords(chats, boutique_stopwords):
    all_stopwords = set(stopwords.words('english')).union(boutique_stopwords)
    output = [removestop(x, all_stopwords) for x in chats]
    return output


# Name removal
def replace_words(text_in, text_a, text_b):
    output = text_in.apply(lambda x: x.replace(text_a, text_b))
    return output


def replace_names(chatlogs, run_remove_names=True):
    """Removes names from the dataset"""

    # If the user specifies that they don't want to run this, skip
    if run_remove_names != True:
        return chatlogs['BODY'].copy()

    output = chatlogs['BODY'].copy()
    for name in [x for x in nltk.corpus.names.words()]:
        output = replace_words(output, ' ' + name + ' ', ' ')
    return output


# endregion

# region Lemmatize and Stem


def lem_n_stem(chats):
    """Do lemmatization keeping only noun, adj, vb, adv, and a snowball stemmer"""
    snowball = SnowballStemmer(language='english')

    # Tokenize things
    texts = [word_tokenize(x) for x in chats]

    # For each user chat in the list
    lemma_chats, stemmed_chats = [], []
    for sent in texts:
        doc = nlp(' '.join(sent))

        # Lemmatize
        doc = [token.lemma_ for token in doc]
        lemma_chats.append(doc)

        # Stem
        doc = [snowball.stem(token) for token in doc]
        stemmed_chats.append(doc)

    # Join things together and export
    lemma_chats = [' '.join(x) for x in lemma_chats]
    stemmed_chats = [' '.join(x) for x in stemmed_chats]

    return lemma_chats, stemmed_chats


# endregion


# region N-Grams

def find_ngrams(input_list, n):
    l_ngrams = list(zip(*[input_list[i:] for i in range(n)]))
    s_ngrams = str(l_ngrams)[1:-1]
    return s_ngrams


def generate_chatlog_with_ngrams(chats):
    """Adds an additional column to the dataframe for all bigrams and trigrams in the chat"""
    bi_grams = [find_ngrams(x.split(' '), 2) for x in chats]
    tri_grams = [find_ngrams(x.split(' '), 3) for x in chats]

    return bi_grams, tri_grams


# endregion

# region User Inputs

def preprocessing(filepath):
    custom_stopwords = ['potato', 'anna', 'I', 'm', '+', 'chat', 'i']

    col_of_interest = 'Live Chat Transcript: Body'
    limit = 8000

    chatlogs_raw = read_in_chatlogs(filepath, col_of_interest, max_chats=limit)
    initial_cleaning = initial_clean_chatlogs(chatlogs_raw, no_numbers=True)

    # TODO: Add in name removal
    # chatlogs['NO_NAMES'] = replace_names(chatlogs, run_remove_names)

    stopwords_removed = remove_all_stopwords(initial_cleaning, custom_stopwords)
    lemmatized, stemmed = lem_n_stem(stopwords_removed)
    bigrams, trigrams = generate_chatlog_with_ngrams(stemmed)

    chatlogs_out = pd.DataFrame({'BODY': initial_cleaning, 'STOPWORDS': stopwords_removed, 'LEMMATIZED': lemmatized,
                                 'STEMMED': stemmed, 'BIGRAMS': bigrams, 'TRIGRAMS': trigrams})

    filename = os.path.basename(filepath)

    # Export to CSV
    chatlogs_out.to_csv('Data/cleaned_'+filename, index=False)


# endregion

cengage_filepath = '/Users/martina.radoslavov/Documents/Clients:Projects/Cengage/cengage-w-intent.csv'

preprocessing(cengage_filepath)
