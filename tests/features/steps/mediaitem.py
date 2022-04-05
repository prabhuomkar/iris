from behave import *


@when('user uploads a "{file_type}" file')
def step_upload_file(context, file_type):
    pass

@then('"{file_type}" file is uploaded')
def step_validate_file_upload(context, file_type):
    pass

@step('metadata for "{file_type}" file is validated')
def step_validate_metadata(context, file_type):
    pass