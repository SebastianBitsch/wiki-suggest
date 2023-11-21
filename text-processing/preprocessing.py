import re
import random
import string
import csv

import numpy as np

from nltk.corpus import stopwords as sw
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

from TFIDF import TFIDF
from utils.read_data import read_articles_file, read_article_ids_file

# TF-IDF parameters
N_TFIDF_FEATURES = 200
N_GRAM_ANALYZER = 'word' # ‘word’, ‘char’, ‘char_wb’
N_MAX_CHARS = 1500

# Translator for removing punctuation, including non unicode U+2013 character "–", very common
punctuation_translator = str.maketrans(string.punctuation + '\u2013', " " * (len(string.punctuation) + 1))

# List of stopwords and a stemmer from nltk that does simple stemming
stemmer = PorterStemmer()
stopwords = set(sw.words("english"))


def remove_numbers(text:str) -> str:
    """ Match all digits in the string and replace them with an empty string """
    new_text = re.sub(r'[0-9]', ' ', text)
    return new_text


def remove_blank_space(text: str) -> str:
    """ Stolen from: https://stackoverflow.com/a/1546244"""
    # return re.sub(' +', ' ', text)        # Doesnt really work
    # return re.sub(' {2,}', ' ', text)     # Doesnt really work
    return " ".join(text.split()) # TODO: Slooowwwwww


def clean(text: str) -> str:
    """ Strip the text of punctutaion, numbers, excessive spaces, etc. """
    text = remove_numbers(text)                                         # remove numbers
    text = text.translate(punctuation_translator)                       # remove punctuation: !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~
    text = text.lower()                                                 # convert to lower case
    text = remove_blank_space(text)                                     # remove double+ spacing
    text = text.strip()                                                 # remove newline characters and spaces
    return text


def preprocess(text: str) -> str:
    """
    Do preprocessing which includes:
        - cleaning text
        - removing stop words
        - stemming words
    """
    text = clean(text)
    
    # Do stop word removal and stemming in one pass, looks messy saves some time
    words = text.split()
    return " ".join([stemmer.stem(word) for word in words if not word in stopwords])


def shorten_texts(corpus: list, max_chars: int = 10_000):
    return [text[:max_chars] for text in corpus]


def random_articles(articles: set, N : int, seed: int = 0) -> set:
    """ Return a subset of N random articles """
    random.seed(seed)
    random_keys = random.sample(list(articles.keys()), N)

    return { key : articles[key] for key in random_keys }



if __name__ == "__main__":
    print("Starting job... ")

    N = None # Read all the data

    article_texts_path = "/work3/s204163/wiki/article_texts"
    article_ids_path = "/work3/s204163/wiki/article_ids"
    clean_texts_path = "/work3/s204163/wiki/cleaned_texts1500"
    tfidf_features_path = "/work3/s204163/wiki/tfidffeatures1500.csv"

    all_articles = read_articles_file(article_texts_path, N = N, read_titles = True)
    article_ids = read_article_ids_file(article_ids_path, N = N)

    print(f"Read {len(all_articles)} articles")
    print("Preprocessing...")
    
    # Preprocess the texts: clean, remove stopwords, stem, etc.
    raw_corpus = list(all_articles.values())
    corpus = [preprocess(text) for text in raw_corpus]

    # Shorten the texts to 
    corpus = shorten_texts(corpus, max_chars = N_MAX_CHARS)

    # Save the cleaned texts
    with open(clean_texts_path, 'w') as result_file:
        wr = csv.writer(result_file)
        wr.writerows(zip(article_ids, corpus))

    # Do tfidf
    print("tf-idf...")

    tfidf = TFIDF(N_TFIDF_FEATURES)
    X = tfidf.vectorize(corpus)
    np.savetxt("/work3/s204163/wiki/tfidffeatures.csv", X, delimiter=",")

    print("Done!")
