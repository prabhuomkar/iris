from .common import get_response


def get_file_name(ext: str):
    return 'pizza.{}'.format(ext.lower())

def upload(context, file_type):
    file_name = get_file_name(file_type)
    with open(f'../data/mediaitem/images/{file_name}', 'rb') as f:
        context.response = get_response(
            query="""
                mutation Upload($file: Upload!) {
                    upload(file: $file): String
                }
            """,
            variables={"file": f},
            upload_files=True
        )

def get_mediaitem(id: str):
    pass

def get_mediaitems():
    pass

def update_mediaitem(id: str, description: str):
    pass

def validate_metadata():
    pass

def validate_uploaded():
    pass