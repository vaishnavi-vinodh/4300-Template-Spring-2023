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


def process_input(query, results, time, diet, course, keywords, data_dict):
    ingr_matrix = tfidf(data_dict, "ingredients")
    # key_matrix = tfidf(data_dict, "description")
    ranked = rank(query, results)
    filtered_time = filter_time(ranked, time)
    filtered_diet = filter_diet(filtered_time, diet)
    return filter_course(filtered_diet, course)


def rocchio(query):
    pass


def tokenize(text):
    text = text.lower()
    return re.findall(r'[a-z]+', text)


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
    np.savetxt("ingr_matrix.csv", doc_by_vocab, delimiter=",")
    #index_to_vocab = {i:v for i, v in enumerate(tfidf_vec.get_feature_names())}
    return doc_by_vocab


def rank(query, results):
    ranks = []
    q = tokenize(query)
    query = set(q)
    for res in results:
        ing = tokenize(res['ingredients'])
        ingredients = set(ing)
        intersection = len((query).intersection(ingredients))
        union = (len(query) + len(ingredients)) - intersection
        ranks.append((float(intersection) / (union*len(ing)*len(q)), res))
    final = sorted(ranks, key=lambda x: x[0])
    return [res for _, res in final][::-1]


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


def sql_search(text, time, diet, course, keywords):
    query_sql = f"""SELECT name, image_url, description, diet, prep_time, ingredients, course, cuisine FROM recipes"""
    keys = ["name", "image_url", "description",
            "diet", "prep_time", "ingredients", "course", "cuisine"]
    data = mysql_engine.query_selector(query_sql)
    data_dict = [dict(zip(keys, i)) for i in data]
    results = process_input(text, data_dict, time, diet,
                            course, keywords, data_dict)
    return json.dumps(results)


@ app.route("/")
def home():
    return render_template('base.html', title="sample html")


@ app.route("/episodes")
def episodes_search():
    text = request.args.get("ingredients")
    keywords = request.args.get("keywords")
    time = request.args.get("time")
    diet = request.args.get("diet")
    course = request.args.get("course")
    return sql_search(text, time, diet, course, keywords)


# app.run(debug=True)
