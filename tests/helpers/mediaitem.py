import json
from .common import get_response


def get_file_name(ext: str):
    return 'sample.{}'.format(ext.lower())

def upload(file_type):
    file_name = get_file_name(file_type)
    with open(f'data/mediaitem/images/{file_name}', 'rb') as f:
        res = get_response(
            query="""
                mutation Upload($file: Upload!) {
                    upload(file: $file)
                }
            """,
            variables={"file": f},
            upload_files=True
        )
        return res['upload'] if res is not None else None

def get_mediaitem(id):
    res = get_response(
        query="""
            query MediaItem($id: String!) {
                mediaItem(id: $id) {
                    id
                    description
                    fileName
                    mimeType
                    fileSize
                    favourite
                    deleted
                    sourceUrl
                    previewUrl
                    mediaMetadata {
                        width
                        height
                        photo {
                            cameraMake
                            cameraModel
                            focalLength
                            apertureFNumber
                            isoEquivalent
                            exposureTime
                        }
                    }
                }
            }
        """,
        variables={"id": id}
    )
    return res['mediaItem'] if res is not None else None

def get_mediaitems():
    res = get_response(
        query="""
            query MediaItems {
                mediaItems {
                    nodes {
                        id
                    }
                }
            }
        """,
        variables={}
    )
    return res['mediaItems']['nodes'] if res is not None else None

def update_mediaitem_description(id, description):
    res = get_response(
        query="""
            mutation UpdateMediaItemDescription($id: String!, $description: String!) {
                updateDescription(id: $id, description: $description)
            }
        """,
        variables={"id": id, "description": description}
    )
    return res['updateDescription'] if res is not None else None

def favourite_mediaitem(id, type):
    res = get_response(
        query="""
            mutation Favourite($id: String!, $type: String!) {
                favourite(id: $id, type: $type)
            }
        """,
        variables={"id": id, "type": type}
    )
    return res['favourite'] if res is not None else None

def get_favourites():
    res = get_response(
        query="""
            query Favourites {
                favourites {
                    nodes {
                        id
                    }
                }
            }
        """,
        variables={}
    )
    return res['favourites']['nodes'] if res is not None else None

def delete_mediaitem(id, type):
    res = get_response(
        query="""
            mutation Delete($id: String!, $type: String!) {
                delete(id: $id, type: $type)
            }
        """,
        variables={"id": id, "type": type}
    )
    return res['delete'] if res is not None else None

def get_deleted():
    res = get_response(
        query="""
            query Deleted {
                deleted {
                    nodes {
                        id
                    }
                }
            }
        """,
        variables={}
    )
    return res['deleted']['nodes'] if res is not None else None

def get_mediaitem_by_file_type(db, mime_type):
    res = db['mediaitems'].find_one({'mimeType': mime_type})
    if res is not None:
        return str(res['_id'])
    return None

def get_expected_metadata(file_type):
    file_name = get_file_name(file_type)
    with open(f'data/mediaitem/metadata/{file_name}.json', 'rb') as f:
        return json.load(f)
