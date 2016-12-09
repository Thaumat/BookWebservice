from flask import Flask, request, redirect, url_for
from flask.ext.pymongo import PyMongo
import json
from flask import render_template
import requests

app = Flask(__name__)
app.config['MONGO_HOST'] = 'localhost'
app.config['MONGO_PORT'] = 27017
app.config['MONGO_DBNAME'] = 'CatWorks'

mongo = PyMongo(app, config_prefix='MONGO')


@app.route('/')
def hello_world():
    works_found = 0
    works = []
    for work in mongo.db.cat_data.find():
        if works_found < 10:
            works_found += 1
            works.append(work)
        else:
            break
    return render_template('index.html', works=works)


@app.route('/search/<search_input>')
def search_results(search_input):


    matching_results = []

    if search_input is not None:
        for work in mongo.db.cat_data.find():
            if search_input in work['title']:
                matching_results.append(work)

    return render_template('search.html', matching_results=matching_results)


@app.route('/works/<work_id>')
def works_page(work_id):
    work = mongo.db.cat_data.find_one({'_id': work_id})
    authors = []
    for author in work['authors']:
        author_data = requests.get(str('https://openlibrary.org' + author['author']['key'] + '.json')).text
        authors.append(author_data)
    work['authors'] = authors
    return render_template('works.html', work=work)


@app.route('/find', methods = ['POST', 'GET'])
def find():
   if request.method == 'POST':
      search_input = request.form['search_input']
      return redirect(url_for('search_results', search_input = search_input))
   else:
       search_input = request.args.get('search_input')
       return redirect(url_for('search_results', search_input = search_input))

if __name__ == '__main__':
    app.run()
