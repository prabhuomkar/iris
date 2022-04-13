from behave import *
from helpers.mediaitem import *
from helpers.common import json_validate_mediaitem


@when('user uploads "{file_type}" file')
def step_upload_file(context, file_type):
    context.file_id = upload(file_type)
    assert context.file_id != None

@then('file is uploaded')
def step_validate_file_upload(context):
    context.response = get_mediaitem(context.file_id)
    assert context.response['id'] == context.file_id

@step('metadata for "{file_type}" file is validated')
def step_validate_metadata(context, file_type):
    exp = get_expected_metadata(file_type)
    context.response = get_mediaitem(context.file_id)
    json_validate_mediaitem(exp, context.response)

@step('user updates "{mime_type}" file')
def step_update_file(context, mime_type):
    context.file_id = get_mediaitem_by_file_type(context.db, mime_type)
    context.response = update_mediaitem_description(context.file_id, 'test-description')
    assert context.response == True

@step('file description is updated')
def step_file_updated(context):
    context.response = get_mediaitem(context.file_id)
    assert context.response['id'] == context.file_id
    assert context.response['description'] == 'test-description'

@step('user favourites "{mime_type}" file')
def step_favourite_file(context, mime_type):
    context.file_id = get_mediaitem_by_file_type(context.db, mime_type)
    context.response = favourite_mediaitem(context.file_id, 'add')
    assert context.response == True

@step('file is marked as favourite')
def step_validate_file_is_marked_favourite(context):
    context.response = get_mediaitem(context.file_id)
    assert context.response['id'] == context.file_id
    assert context.response['favourite'] == True

@step('file is listed in favourites')
def step_validate_file_in_favourites(context):
    context.response = get_favourites()
    ids = [node['id'] for node in context.response]
    assert context.file_id in ids

@step('user unfavourites "{mime_type}" file')
def step_favourite_file(context, mime_type):
    context.file_id = get_mediaitem_by_file_type(context.db, mime_type)
    context.response = favourite_mediaitem(context.file_id, 'remove')
    assert context.response == True

@step('file is not marked as favourite')
def step_validate_file_is_not_marked_favourite(context):
    context.response = get_mediaitem(context.file_id)
    assert context.response['id'] == context.file_id
    assert context.response['favourite'] == False

@step('file is not listed in favourites')
def step_validate_file_in_favourites(context):
    context.response = get_favourites()
    ids = [node['id'] for node in context.response]
    assert context.file_id not in ids

@step('user deletes "{mime_type}" file')
def step_delete_file(context, mime_type):
    context.file_id = get_mediaitem_by_file_type(context.db, mime_type)
    context.response = delete_mediaitem(context.file_id, 'add')
    assert context.response == True

@step('file is marked as deleted')
def step_validate_file_is_marked_deleted(context):
    context.response = get_mediaitem(context.file_id)
    assert context.response['id'] == context.file_id
    assert context.response['deleted'] == True

@step('file is listed in trash')
def step_validate_file_in_trash(context):
    context.response = get_deleted()
    ids = [node['id'] for node in context.response]
    assert context.file_id in ids

@step('user undeletes "{mime_type}" file')
def step_permanently_delete_file(context, mime_type):
    context.file_id = get_mediaitem_by_file_type(context.db, mime_type)
    context.response = delete_mediaitem(context.file_id, 'remove')
    assert context.response == True

@step('file is not marked as deleted')
def step_validate_file_is_not_marked_deleted(context):
    context.response = get_mediaitem(context.file_id)
    assert context.response['id'] == context.file_id
    assert context.response['deleted'] == False

@step('user permanently deletes "{mime_type}" file')
def step_permanently_delete_file(context, mime_type):
    context.file_id = get_mediaitem_by_file_type(context.db, mime_type)
    context.response = delete_mediaitem(context.file_id, 'permanent')
    assert context.response == True

@step('file is deleted')
def step_validate_file_is_deleted(context):
    context.response = get_mediaitem(context.file_id)
    assert context.response == None

@step('file is not listed in trash')
def step_validate_file_not_in_trash(context):
    context.response = get_deleted()
    ids = [node['id'] for node in context.response]
    assert context.file_id not in ids
