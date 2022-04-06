from typing import Dict
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


transport = AIOHTTPTransport(url="http://localhost:5001/graphql")
client = Client(transport=transport, fetch_schema_from_transport=True)

def get_response(query: str, variables: Dict, upload_files: bool = False):
    query = gql(query)
    return client.execute(query)
