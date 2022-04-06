from behave import *
from pymongo import MongoClient
import requests


def before_all(context):
    # establish database connection
    client = MongoClient('mongodb://root:root@localhost:5010/skim?authSource=admin')
    db = client['iris']
    context.db = db

def after_all(context):
    print(' START CLEARING DATA '.center(80, '*'))

    # get mediaitems to clear from cdn
    mediaitems_to_clear = []
    cursor = context.db['mediaitems'].find({})
    for document in cursor:
        if 'thumbnailUrl' in document:
            mediaitems_to_clear.append(document['thumbnailUrl'])
        if 'sourceUrl' in document:
            mediaitems_to_clear.append(document['sourceUrl'])
    cursor = context.db['albums'].find({})
    for document in cursor:
        if 'thumbnailUrl' in document:
            mediaitems_to_clear.append(document['thumbnailUrl'])
    cursor = context.db['entities'].find({})
    for document in cursor:
        if 'thumbnailUrl' in document:
            mediaitems_to_clear.append(document['thumbnailUrl'])

    # clear all collections
    print(f"clearing {context.db['mediaitems'].count_documents({})} mediaitems")
    context.db['mediaitems'].drop()
    print(f"clearing {context.db['entities'].count_documents({})} entities")
    context.db['entities'].drop()
    print(f"clearing {context.db['albums'].count_documents({})} albums")
    context.db['albums'].drop()

    # clear all mediaitems from cdn
    print(f'clearing {len(mediaitems_to_clear)} cdn files')
    for mediaitem in mediaitems_to_clear:
        requests.delete(mediaitem)
    print(' FINISH CLEARING DATA '.center(80, '*'))
