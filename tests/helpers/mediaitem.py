from .common import get_response


def get_file_name(ext: str):
    return 'pizza.{}'.format(ext.lower())

def upload(file_type):
    file_name = get_file_name(file_type)
    with open(f'data/mediaitem/images/{file_name}', 'rb') as f:
        response = get_response(
            query="""
                mutation Upload($file: Upload!) {
                    upload(file: $file)
                }
            """,
            variables={"file": f},
            upload_files=True
        )
        file_id = response['upload']
        return file_id

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
                }
            }
        """,
        variables={"id": id}
    )
    return res['mediaItem']

def get_mediaitems():
    pass

def update_mediaitem_description(id, description):
    res = get_response(
        query="""
            mutation UpdateMediaItemDescription($id: String!, $description: String!) {
                updateDescription(id: $id, description: $description)
            }
        """,
        variables={"id": id, "description": description}
    )
    return res['updateDescription']

def validate_uploaded():
    pass

def get_mediaitem_by_file_type(db, mime_type):
    res = db['mediaitems'].find_one({'mimeType': mime_type})
    return str(res['_id'])
