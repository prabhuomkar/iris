from time import sleep
from behave import *


@step('api service is running')
def step_service_is_running(context):
    pass

@step('worker service is running')
def step_service_is_running(context):
    pass

@step('waits for "{time}" seconds')
def step_wait(context, time):
    sleep(float(time))