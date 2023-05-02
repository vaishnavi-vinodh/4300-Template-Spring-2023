import json
import os
from flask import Flask, render_template, request
from flask_cors import CORS
from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler
from collections import Counter
from collections import defaultdict
import math
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


def tokenize(text):
    text = text.lower()
    return re.findall(r'[a-z]+', text)


def build_inverted_index(data):
    inverted_index = {}
    for doc_id, d in enumerate(data):
        counts = Counter(tokenize(d['description']))
        for word in counts:
            if word in inverted_index:
                inverted_index[word].append((doc_id, counts[word]))
            else:
                inverted_index[word] = [(doc_id, counts[word])]
    with open('postings_key.csv', 'w') as f:
        for key in inverted_index.keys():
            f.write("%s,%s\n" % (key, inverted_index[key]))


def build_vectorizer(max_features=5000, stop_words="english", max_df=0.8, min_df=5, norm='l2'):
    vectorizer = TfidfVectorizer(
        max_features=max_features, stop_words=stop_words, max_df=max_df, min_df=min_df, norm=norm)
    return vectorizer


def tfidf(recipes, field):
    n_feats = 5000
    tfidf_vec = build_vectorizer()
    doc_by_vocab = np.empty([len(recipes), n_feats])
    doc_by_vocab = tfidf_vec.fit_transform(
        [r[field] for r in recipes]).toarray()
    np.savetxt("key_matrix.csv", doc_by_vocab, delimiter=",")
    index_to_vocab = {i: v for i, v in enumerate(
        tfidf_vec.get_feature_names())}
    with open('index_to_key.csv', 'w') as f:
        for key in index_to_vocab.keys():
            f.write("%s,%s\n" % (key, index_to_vocab[key]))
    return doc_by_vocab
