from behave import *
from pymongo import MongoClient
import requests


def before_all(context):
    # establish database connection
    client = MongoClient('mongodb://root:root@localhost:5010/skim?authSource=admin')
    db = client['iris']
    context.db = db
    clear_data(context)

def after_feature(context, feature):
    clear_data(context)

def clear_data(context):
    # get mediaitems to clear from cdn
    mediaitems_to_clear = []
    cursor = context.db['mediaitems'].find({})
    for document in cursor:
        if 'previewURL' in document and len(document['previewURL']) > 0:
            mediaitems_to_clear.append(document['previewURL'])
        if 'sourceUrl' in document and len(document['sourceUrl']) > 0:
            mediaitems_to_clear.append(document['sourceUrl'])
    cursor = context.db['albums'].find({})
    for document in cursor:
        if 'previewURL' in document and len(document['previewURL']) > 0:
            mediaitems_to_clear.append(document['previewURL'])
    cursor = context.db['entities'].find({})
    for document in cursor:
        if 'previewURL' in document and len(document['previewURL']) > 0:
            mediaitems_to_clear.append(document['previewURL'])

    # clear all collections
    context.db['mediaitems'].drop()
    context.db['entities'].drop()
    context.db['albums'].drop()

    # clear all mediaitems from cdn
    for mediaitem in mediaitems_to_clear:
        requests.delete(mediaitem)
