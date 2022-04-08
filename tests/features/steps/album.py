from behave import *
from helpers.album import *
from helpers.mediaitem import get_mediaitems


@step('user creates an album')
def step_album_create(context):
    context.response = get_mediaitems()
    context.file_ids = [node['id'] for node in context.response]
    context.album_id = create_album('album-name', 'album-description', context.file_ids[:2])
    assert context.album_id != None

@step('user updates an album')
def step_album_update(context):
    context.album_id = get_album_by_name(context.db, 'album-name')
    context.response = update_album(context.album_id, 'album-new-name', 'album-new-description')
    assert context.response == True

@step('user "{type}" album mediaitems')
def step_album_update_mediaitems(context, type):
    type = type[:-1]
    context.album_id = get_album_by_name(context.db, 'album-new-name')
    context.response = get_mediaitems()
    context.file_ids = [node['id'] for node in context.response]
    context.response = update_album_mediaitems(context.album_id, type, context.file_ids[2:])
    assert context.response == True

@step('user updates an album preview mediaitem')
def step_album_update_preview_mediaitem(context):
    context.album_id = get_album_by_name(context.db, 'album-new-name')
    context.response = get_mediaitems()
    context.file_ids = [node['id'] for node in context.response]
    context.response = update_album_preview_url(context.album_id, context.file_ids[2])
    assert context.response == True

@step('user deletes an album')
def step_album_delete(context):
    context.album_id = get_album_by_name(context.db, 'album-new-name')
    context.response = delete_album(context.album_id)
    assert context.response == True

@step('album is created')
def step_validate_album_created(context):
    context.response = get_album(context.album_id)
    assert context.response['id'] == context.album_id
    assert context.response['name'] == 'album-name'
    assert context.response['description'] == 'album-description'
    assert context.response['mediaItems']['totalCount'] == 2

@step('album is updated')
def step_validate_album_updated(context):
    context.response = get_album(context.album_id)
    assert context.response['id'] == context.album_id
    assert context.response['name'] == 'album-new-name'
    assert context.response['description'] == 'album-new-description'
    assert context.response['mediaItems']['totalCount'] == 2

@step('album preview mediaitem is updated')
def step_validate_album_preview_mediaitem_updated(context):
    context.response = get_album(context.album_id)
    assert context.response['id'] == context.album_id

@step('album mediaitems are updated after "{type}"')
def step_validate_album_mediaitems_updated(context, type):
    type = type[:-3]
    context.response = get_album(context.album_id)
    assert context.response['id'] == context.album_id
    assert context.response['mediaItems']['totalCount'] == 5 if type == 'add' else 2

@step('album is deleted')
def step_validate_album_deleted(context):
    context.response = get_album(context.album_id)
    assert context.response == None

@step('album is listed in albums')
def step_album_listed_in_albums(context):
    context.response = get_albums()
    ids = [node['id'] for node in context.response]
    assert context.album_id in ids

@step('album is not listed in albums')
def step_album_not_listed_in_albums(context):
    context.response = get_albums()
    ids = [node['id'] for node in context.response]
    assert context.album_id not in ids
