from .common import get_response
from .mediaitem import get_mediaitem_by_file_type


def get_albums():
    res = get_response(
        query="""
            query Albums {
                albums {
                    nodes {
                        id
                    }
                }
            }
        """,
        variables={}
    )
    return res['albums']['nodes'] if res is not None else None

def get_album(id):
    res = get_response(
        query="""
            query Album($id: String!) {
                album(id: $id) {
                    id
                    description
                    name
                    mediaItems {
                        totalCount
                    }
                }
            }
        """,
        variables={"id": id}
    )
    return res['album'] if res is not None else None

def create_album(name, description, media_items):
    res = get_response(
        query="""
            mutation CreateAlbum($input: CreateAlbumInput!) {
                createAlbum(input: $input)
            }
        """,
        variables={"input": {"name": name, "description": description, "mediaItems": media_items}}
    )
    return res['createAlbum'] if res is not None else None

def update_album(id, name, description):
    res = get_response(
        query="""
            mutation CreateAlbum($id: String!, $input: UpdateAlbumInput!) {
                updateAlbum(id: $id, input: $input)
            }
        """,
        variables={"id": id, "input": {"name": name, "description": description}}
    )
    return res['updateAlbum'] if res is not None else None

def update_album_thumbnail(id, media_item):
    res = get_response(
        query="""
            mutation UpdateAlbumThumbnailUrl($id: String!, $mediaItemId: String!) {
                updateAlbumThumbnailUrl(id: $id, mediaItemId: $mediaItemId)
            }
        """,
        variables={"id": id, "mediaItemId": media_item}
    )
    return res['updateAlbumThumbnailUrl'] if res is not None else None

def update_album_mediaitems(id, type, media_items):
    res = get_response(
        query="""
            mutation UpdateAlbumMediaItems($id: String!, $type: String!, $mediaItems: [String!]!) {
                updateAlbumMediaItems(id: $id, type: $type, mediaItems: $mediaItems)
            }
        """,
        variables={"id": id, "type": type, "mediaItems": media_items}
    )
    return res['updateAlbumMediaItems'] if res is not None else None

def delete_album(id):
    res = get_response(
        query="""
            mutation DeleteAlbum($id: String!) {
                deleteAlbum(id: $id)
            }
        """,
        variables={"id": id}
    )
    return res['deleteAlbum'] if res is not None else None

def get_album_by_name(db, album_name):
    res = db['albums'].find_one({'name': album_name})
    if res is not None:
        return str(res['_id'])
    return None
