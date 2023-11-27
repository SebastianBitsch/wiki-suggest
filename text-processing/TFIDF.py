import numpy as np
import pandas as pd
import math

from collections import Counter
from collections import Counter


class TFIDF():
    def __init__(self, max_features=None) -> None:
        self.max_features = max_features
        self.tfdic = {}
        self.idfdic = {}

    '''
    Make a dictionary of term frequencies. Where each document has an index which holds
    a dictionary of words as keys number of times it is in the text as a value.
    The value of all words is devided by the value of the most frequent word.
    '''
    def _term_frequency_dic(self, text:str, idx:int):

        # self.tfdic[idx] = {}
        # for word1 in set(text.split()):
        #     self.tfdic[idx][word1] = 0
        #     for word2 in text.split():
        #         if word1 == word2:
        #             self.tfdic[idx][word1] += 1
        # max_val = max(self.tfdic[idx].values())
        # for k,v in zip(self.tfdic[idx].keys(),self.tfdic[idx].values()):
        #     self.tfdic[idx][k] = v/max_val
        word_counts = Counter(text.split())
        max_val = max(word_counts.values())
        self.tfdic[idx] = {word: count / max_val for word, count in word_counts.items()}


    
    '''
    Make a dictionary of inverse document frequencies. 
    Here each key is the set of words of all texts. 
    The values are the number of time each of the words appear in a document

    IDF_i = log2(N/n_i)
    N is the number of documents, n_i is the number of documents the word is in
    We add a 1 to not divide by zero
    '''
    def _inverse_doc_freq(self, texts):
        doc_count = len(texts)

        # words = set(word for text in texts for word in text.split())
        # for word in words:
        #     df = sum(word in text for text in texts)
        #     # self.idfdic[word] = math.log(doc_count / (1 + df))
        #     ### Use smoothing like sklearn in order to avoid zero division
        #     self.idfdic[word] = math.log(1+doc_count) - math.log((1+ df))+1

        word_document_counts = Counter(word for text in texts for word in set(text.split()))
        self.idfdic = {word: math.log(1 + doc_count) - math.log(1 + df) + 1 for word, df in word_document_counts.items()}

        ### Use only the max number of features
        if self.max_features is not None:
            sorted_terms = sorted(self.idfdic.items(), key=lambda x: x[1], reverse=True)
            self.idfdic = dict(sorted_terms[:self.max_features])

    '''
    Make the dictionaries
    '''                 
    def _fit(self, texts):
        for i, text in enumerate(texts):
            self._term_frequency_dic(text,i)
        self._inverse_doc_freq(texts)
    '''
    In order to work with the data, we need to return a matrix.
    In which the texts are TF-IDF vectorized
    TF*IDF
    '''
    def _transform(self, texts):
        ### Sort the set in order to get the same sequence every time
        all_words = sorted(set(word for text in texts for word in text.split()))
        tfidf_matrix = []
        for i, text in enumerate(texts):
            tfidf_vector = []
            for word in all_words:
                if word in self.idfdic:  
                    tf = self.tfdic[i].get(word,0)
                    idf = self.idfdic[word]
                    tfidf_vector.append(tf * idf)
            tfidf_matrix.append(tfidf_vector)
        tfidf_matrix = np.array(tfidf_matrix)
        ### L2 normalization as per sklearn process
        l2_norms = np.sqrt((tfidf_matrix ** 2).sum(axis=1, keepdims=True))
        ### No zero divison
        l2_norms[l2_norms == 0] = 1
        tfidf_matrix = tfidf_matrix / l2_norms
        return tfidf_matrix


    def vectorize(self, texts):
        self._fit(texts)
        return self._transform(texts)

