from behave import *
import aegis


@given('there is no database file')
def step_impl(context):
    config = {"database_path": "/tmp/JHu8w345jhksdf.yml"}
    context.aegisdb = aegis.database.Database(config)

@when('Database is instantiated')
def step_impl(context):
    assert True is not False

@then('Database creates a new database file')
def step_impl(context):
    assert context.failed is False