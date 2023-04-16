import json
import os
from flask import Flask, render_template, request
from flask_cors import CORS
from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler

# ROOT_PATH for linking with all your files.
# Feel free to use a config.py or settings.py with a global export variable
os.environ['ROOT_PATH'] = os.path.abspath(os.path.join("..", os.curdir))

# These are the DB credentials for your OWN MySQL
# Don't worry about the deployment credentials, those are fixed
# You can use a different DB name if you want to
MYSQL_USER = "root"
MYSQL_USER_PASSWORD = ""
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


def jaccard(query, results):
    ranks = []
    query = set(query.lower().split(' '))
    for res in results:
        name = set(res['name'].lower().split(' '))
        intersection = len((query).intersection(name))
        union = (len(query) + len(name)) - intersection
        ranks.append((float(intersection) / union, res))
    final = sorted(ranks, key=lambda x: x[0])[-3:][::-1]
    return [res for _, res in final]


def sql_search(episode):
    query_sql = f"""SELECT name, image_url, description FROM recipes"""
    keys = ["name","image_url", "description", "cuisine"]
    data = mysql_engine.query_selector(query_sql)
    results = [dict(zip(keys, i)) for i in data]
    jac = jaccard(episode, results)
    return json.dumps(jac)


@ app.route("/")
def home():
    return render_template('base.html', title="sample html")


@ app.route("/episodes")
def episodes_search():
    text = request.args.get("name")
    return sql_search(text)

# app.run(debug=True)
