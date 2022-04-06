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
                    fileName
                    mimeType
                    fileSize
                }
            }
        """,
        variables={"id": id},
        upload_files=False
    )
    assert res['mediaItem']['id'] == id
    return res['mediaItem']

def get_mediaitems():
    pass

def update_mediaitem(id, description):
    pass

def validate_metadata(res, exp):
    exp = exp.split(',')
    assert res['mimeType'] == exp[0]
    assert str(res['fileSize']) == exp[1]

def validate_uploaded():
    pass