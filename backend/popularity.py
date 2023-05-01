import requests
from bs4 import BeautifulSoup
from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler
import csv
import os
from helpers.MySQLDatabaseHandler import MySQLDatabaseHandler
from collections import defaultdict

os.environ['ROOT_PATH'] = os.path.abspath(os.path.join("..", os.curdir))

MYSQL_USER = "root"
MYSQL_USER_PASSWORD = "flavors"
MYSQL_PORT = 3306
MYSQL_DATABASE = "kardashiandb"
DEFAULT_POP = 700

mysql_engine = MySQLDatabaseHandler(
    MYSQL_USER, MYSQL_USER_PASSWORD, MYSQL_PORT, MYSQL_DATABASE)
# Path to init.sql file. This file can be replaced with your own file for testing on localhost, but do NOT move the init.sql file
mysql_engine.load_file_into_db()


pop_vals = [] 

def generate_url(name):
    new_name = ""
    i = 0
    while i < len(name):
        if (name[i].isalpha()):
            new_name += name[i]
        else:
            if (i > 0 and new_name[len(new_name) - 1] != '-'):
                 new_name += "-"
        i+=1
    if(new_name[-1]=='-'):
        new_name = new_name[:-1]
                
    url = 'https://www.archanaskitchen.com/' + new_name
    print(url)
    return url 


def popularity(url):
    # returns the string representation of the number of ratings
    print("in popularity")
    data = requests.get(url)
    # print("data recieved")
    html = BeautifulSoup(data.text, 'html.parser')
    # print("bs object created")
    popularity = html.select('#recipenumvotes')
    # print("got popularity")
    return popularity

def generate_pops():
    query_sql = f"""SELECT name, image_url, description, diet, prep_time, ingredients, cuisine FROM recipes"""
    keys = ["name", "image_url", "description",
            "diet", "prep_time", "ingredients", "cuisine"]
    data = mysql_engine.query_selector(query_sql)
    data_dict = [dict(zip(keys, i)) for i in data]
    i = 1000
    while i<len(data_dict):
        d = data_dict[i]
        print("generating info for "+ d['name'])
        url = generate_url(d['name'])
        pop = popularity(url)
        if pop == []:
            pop = DEFAULT_POP
        # print(pop)
        pop_dict = {"name": d['name'],"popularity": pop}
        pop_vals.append(pop_dict)
        i+=1

    # for d in data_dict:
    #     url = generate_url(d['name'])
    #     pop = popularity(url)
    #     pop_dict = {"name": d['name'],"pop": pop}
    #     pop_vals.append(pop_dict)

generate_pops()

csv_columns = ['name', 'popularity']
csv_file = "Pops4.csv"

try:
     with open(csv_file, 'w') as csvfile:
          writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
          writer.writeheader()
          for data in pop_vals:
               writer.writerow(data)
except IOError:
     print("I/O error")