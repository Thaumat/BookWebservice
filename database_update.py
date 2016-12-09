import json
from pymongo import MongoClient
import requests


def main():
    client = MongoClient('localhost', 27017)
    database = client['CatWorks']
    cat_data_collection = database['cat_data']

    # '/home/ec2-user/untitled3/cat-works.txt'  Old Path

    file = open('/home/ec2-user/untitled3/cat-works.txt', 'r').read().split('\t')
    for obj in file:
        if 'created' in obj:
            obj = obj.replace('/type/work', '')

            json_obj = json.loads(obj)
            json_obj['_id'] = json_obj['key'].replace('/works/', '')
            cat_data_collection.insert(json_obj)
            '''
            author_modified = []
            for author in json_obj.get('authors', []):
                author_url = 'https://openlibrary.org' + author['author']['key'] + '.json'
                author_result = requests.get(author_url).text
                author_data = json.loads(author_result)
                author_data['key'] = author['author']['key']
                author_modified.append(author_data)
            json_obj['authors'] = author_modified

            '''


if __name__ == '__main__':
    main()