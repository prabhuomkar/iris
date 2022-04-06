from behave import *


@when('user creates an album')
def step_album_create(context):
    pass

@when('user updates an album')
def step_album_update(context):
    pass

@when('user updates an album mediaitems')
def step_album_update_mediaitems(context):
    pass

@when('user deletes an album')
def step_album_delete(context):
    pass

@then('album is created')
def step_validate_album_created(context):
    pass

@then('album is updated')
def step_validate_album_updated(context):
    pass

@then('album is deleted')
def step_validate_album_deleted(context):
    pass

@step('mediaitems are listed in albums')
def step_validate_album_mediaitems(context):
    pass
