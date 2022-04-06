from behave import *
from pymongo import MongoClient
import requests


def after_all(context):
    print(' START CLEARING DATA '.center(80, '*'))
    # establish database connection
    client = MongoClient('mongodb://root:root@localhost:5010/skim?authSource=admin')
    db = client['iris']

    # get mediaitems to clear from cdn
    mediaitems_to_clear = []
    cursor = db['mediaitems'].find({})
    for document in cursor:
        if 'thumbnailUrl' in document:
            mediaitems_to_clear.append(document['thumbnailUrl'])
        if 'sourceUrl' in document:
            mediaitems_to_clear.append(document['sourceUrl'])
    cursor = db['albums'].find({})
    for document in cursor:
        if 'thumbnailUrl' in document:
            mediaitems_to_clear.append(document['thumbnailUrl'])
    cursor = db['entities'].find({})
    for document in cursor:
        if 'thumbnailUrl' in document:
            mediaitems_to_clear.append(document['thumbnailUrl'])

    # clear all collections
    print(f"clearing {db['mediaitems'].count_documents({})} mediaitems")
    db['mediaitems'].drop()
    print(f"clearing {db['entities'].count_documents({})} entities")
    db['entities'].drop()
    print(f"clearing {db['albums'].count_documents({})} albums")
    db['albums'].drop()

    # clear all mediaitems from cdn
    print(f'clearing {len(mediaitems_to_clear)} cdn files')
    for mediaitem in mediaitems_to_clear:
        requests.delete(mediaitem)
    print(' FINISH CLEARING DATA '.center(80, '*'))
