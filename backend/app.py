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
import pandas as pd


# ROOT_PATH for linking with all your files.
# Feel free to use a config.py or settings.py with a global export variable
os.environ['ROOT_PATH'] = os.path.abspath(os.path.join("..", os.curdir))

# These are the DB credentials for your OWN MySQL
# Don't worry about the deployment credentials, those are fixed
# You can use a different DB name if you want to
MYSQL_USER = "root"
MYSQL_USER_PASSWORD = "flavors"
MYSQL_PORT = 3306
MYSQL_DATABASE = "kardashiandb"

ALPHA = 0.7
BETA = 0.98
GAMMA = 0.28
DELTA = 0.000000001

mysql_engine = MySQLDatabaseHandler(
    MYSQL_USER, MYSQL_USER_PASSWORD, MYSQL_PORT, MYSQL_DATABASE)

# Path to init.sql file. This file can be replaced with your own file for testing on localhost, but do NOT move the init.sql file
mysql_engine.load_file_into_db()

app = Flask(__name__)
CORS(app)

# Sample search, the LIKE operator in this case is hard-coded,
# but if you decide to use SQLAlchemy ORM framework,
# there's a much better and cleaner way to do this

TIME_START_INDEX = 9
TIME_END_INDEX = -2


def process_input(query_ingredients, query_keywords, results, time, diet, course):
    # TODO: account for keywords being blank/needing to be weighted less
    n_docs = len(results)
    index_to_key, postings_key, popularity = read_csvs()
    idf = compute_idf(postings_key, n_docs)
    keyword_cossim = cossim(query_keywords, postings_key,
                            idf, index_to_key, n_docs)
    ingredient_jaccard = jaccard(query_ingredients, results)
    sorted = rank(results, keyword_cossim, ingredient_jaccard, popularity)
    ranked = [results[i] for i, _ in sorted]
    filtered_time = filter_time(ranked, time)
    filtered_diet = filter_diet(filtered_time, diet)
    return filter_course(filtered_diet, course)


def rank(results, keyword_cossim, ingredient_jaccard, popularity):
    scores = {}
    # TODO: Check empty ingredients
    print(keyword_cossim)
    print(ingredient_jaccard)
    key_list = [v for _, v in keyword_cossim]
    ingr_list = [v for _, v in ingredient_jaccard]
    print(key_list)
    print(ingr_list)
    for id in range(len(results)):
        if id in keyword_cossim and id in ingr_list:
            scores[id] = ALPHA * ingredient_jaccard[id][0] + GAMMA * \
                keyword_cossim[id] + \
                (DELTA * popularity[id])
        elif id in keyword_cossim:
            scores[id] = BETA * keyword_cossim[id] + \
                (DELTA * popularity[id])
        elif id in ingr_list:
            scores[id] = BETA * ingredient_jaccard[id][0] + \
                (DELTA * popularity[id])
        else:
            scores[id] = DELTA * popularity[id]
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


def read_csvs():
    index_to_key = clean_dict((pd.read_csv('index_to_key.csv', usecols=[
                               'index', 'word']).to_dict(orient="records")), 'index', 'word')
    postings_key = clean_dict((pd.read_csv('postings_key.csv', usecols=[
        'word', 'postings']).to_dict(orient="records")), 'word', 'postings')
    popularity = {k: int(v['popularity']) for k, v in (pd.read_csv('popularity.csv', usecols=[
        'name', 'popularity']).to_dict(orient="index")).items()}
    return index_to_key, postings_key, popularity


def string_to_list(str):
    result = []
    for element in re.findall('\(.*?\)', str):
        element = element[1:-1].split(',')
        result.append((int(element[0]), int(element[1])))
    return result


def clean_dict(list, col1, col2):
    result = {}
    for dict in list:
        result[dict[col1]] = dict[col2]
    return result


def tokenize(text):
    text = text.lower()
    return re.findall(r'[a-z]+', text)


def compute_doc_norms(postings, idf, n_docs):
    norms = np.zeros(n_docs)
    for word in postings:
        if word in idf:
            idf_i = idf[word]
            post = string_to_list(postings[word])
            for j, tf_ij in post:
                norms[j] += (tf_ij * idf_i) ** 2

    norms = np.sqrt(norms)
    return norms


def dot_products(query_word_counts, postings, idf):
    doc_scores = {}
    for word in query_word_counts:
        if word in postings:
            post = string_to_list(postings[word])
            for posting in post:
                w_ij = posting[1] * idf[word]
                w_iq = query_word_counts[word] * idf[word]
                doc_scores[posting[0]] = doc_scores.get(
                    posting[0], 0) + w_ij * w_iq
    return doc_scores


def compute_idf(inv_idx, n_docs):
    idf = {}
    for word in inv_idx:
        df = len(inv_idx[word])
        term_idf = math.log2(n_docs/(1 + df))
        idf[word] = term_idf
    return idf


def cossim(query, postings, idf, index_to_key, n_docs):
    key_to_index = {v: k for k, v in index_to_key.items()}
    results = []
    query_word_counts = Counter(tokenize(query.lower()))
    numerators = dot_products(query_word_counts, postings, idf)
    query_norm = 0
    for word in query_word_counts:
        if word in key_to_index:
            query_norm += (query_word_counts[word] * idf[word]) ** 2
    query_norm = math.sqrt(query_norm)

    doc_norms = compute_doc_norms(postings, idf, n_docs)
    for doc_id in numerators:
        num = numerators[doc_id]
        doc_norm = doc_norms[doc_id]
        score = num / (doc_norm * query_norm)
        results.append((score, doc_id))
    return results


def jaccard(query, results):
    result = []
    q = tokenize(query)
    query = set(q)
    for id, res in enumerate(results):
        ing = tokenize(res['ingredients'])
        ingredients = set(ing)
        intersection = len((query).intersection(ingredients))
        union = (len(query) + len(ingredients)) - intersection
        result.append((float(intersection) / (union*len(ing)*len(q)), id))

    return result


def filter_time(results, time):
    filtered = []
    for res in results:
        if res['prep_time']:
            res_time = res['prep_time'][TIME_START_INDEX:TIME_END_INDEX]
            if int(res_time) <= int(time):
                filtered.append(res)
    return filtered


def filter_course(results, course):
    filtered = []
    for res in results:
        res_course = res['course']
        if course in res_course or course == 'Click dropdown':
            filtered.append(res)
        if len(filtered) == 3:
            break
    return filtered


def filter_diet(results, diet):
    filtered = []
    for res in results:
        res_diet = res['diet']
        if res_diet == diet or diet == 'Non-Vegetarian':
            filtered.append(res)
    return filtered


def sql_search(query_ingredients, query_keywords, time, diet, course):
    query_sql = f"""SELECT name, image_url, description, diet, prep_time, ingredients, course, cuisine FROM recipes"""
    keys = ["name", "image_url", "description",
            "diet", "prep_time", "ingredients", "course", "cuisine"]
    data = mysql_engine.query_selector(query_sql)
    data_dict = [dict(zip(keys, i)) for i in data]
    results = process_input(query_ingredients, query_keywords, data_dict, time, diet,
                            course)
    return json.dumps(results)


@ app.route("/")
def home():
    return render_template('base.html', title="sample html")


@ app.route("/episodes")
def episodes_search():
    query_ingredients = request.args.get("ingredients")
    query_keywords = request.args.get("keywords")
    time = request.args.get("time")
    diet = request.args.get("diet")
    course = request.args.get("course")
    return sql_search(query_ingredients, query_keywords, time, diet, course)


# app.run(debug=True)
