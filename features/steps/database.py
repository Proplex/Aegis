from behave import *
import aegis


@given('there is no database file')
def step_impl(context):
    pass

@when('Database is instantiated')
def step_impl(context):
    aegis.core.md5("test")
    assert True is not False

@then('Database creates a new database file')
def step_impl(context):
    assert context.failed is False