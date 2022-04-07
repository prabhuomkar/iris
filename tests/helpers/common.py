from typing import Dict
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


transport = AIOHTTPTransport(url="http://localhost:5001/graphql")
client = Client(transport=transport, fetch_schema_from_transport=True)

def get_response(query: str, variables: Dict, upload_files: bool = False):
    try:
        query = gql(query)
        return client.execute(query, variable_values=variables, upload_files=upload_files)
    except:
        return None

def json_validate_mediaitem(exp: Dict, got: Dict):
    assert exp['fileSize'] == got['fileSize']
    assert exp['mimeType'] == got['mimeType']
    assert exp['mediaMetadata']['width'] == got['mediaMetadata']['width']
    assert exp['mediaMetadata']['height'] == got['mediaMetadata']['height']
    if 'photo' in exp['mediaMetadata']:
        for meta_type in ['cameraMake', 'cameraModel', 'focalLength', 'apertureFNumber', 'isoEquivalent', 'exposureTime']:
            if meta_type in exp['mediaMetadata']['photo']:
                assert exp['mediaMetadata']['photo'][meta_type] == got['mediaMetadata']['photo'][meta_type]