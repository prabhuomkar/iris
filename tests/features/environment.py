from behave import *
from pymongo import MongoClient
import requests


def before_all(context):
    # establish database connection
    client = MongoClient('mongodb://root:root@localhost:5010/skim?authSource=admin')
    db = client['iris']
    context.db = db

def after_feature(context, feature):
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
    context.db['mediaitems'].drop()
    context.db['entities'].drop()
    context.db['albums'].drop()

    # clear all mediaitems from cdn
    for mediaitem in mediaitems_to_clear:
        requests.delete(mediaitem)
