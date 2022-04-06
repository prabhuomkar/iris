from behave import *
from helpers.mediaitem import *


@step('user uploads "{file_type}" file')
def step_upload_file(context, file_type):
    upload
    pass

@step('"{file_type}" file is uploaded')
def step_validate_file_upload(context, file_type):
    pass

@step('metadata for "{file_type}" file is validated')
def step_validate_metadata(context, file_type):
    pass

@step('user updates "{file_type}" file')
def step_update_file(context, file_type):
    pass

@step('"{file_type}" file is updated')
def step_file_updated(context, file_type):
    pass

@step('user favourites "{file_type}" file')
def step_favourite_file(context, file_type):
    pass

@step('"{file_type}" file is marked as favourite')
def step_validate_file_is_marked_favourite(context, file_type):
    pass

@step('"{file_type}" is listed in favourites')
def step_validate_file_in_favourites(context, file_type):
    pass

@step('user deletes "{file_type}" file')
def step_delete_file(context, file_type):
    pass

@step('"{file_type}" file is marked as deleted')
def step_validate_file_is_marked_deleted(context, file_type):
    pass

@step('"{file_type}" is listed in trash')
def step_validate_file_in_trash(context, file_type):
    pass

@step('user permanently deletes "{file_type}" file')
def step_permanently_delete_file(context, file_type):
    pass

@step('"{file_type}" file is deleted')
def step_validate_file_is_deleted(context, file_type):
    pass

@step('"{file_type}" is not listed in trash')
def step_validate_file_not_in_trash(context, file_type):
    pass
