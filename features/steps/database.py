from behave import *
from unittest import mock
import aegis, uuid

def fake_function():
    return

@given('there is no database file')
def step_impl(context):
    context.random_file = f"/tmp/{str(uuid.uuid4())[0:5]}.yml"
    context.config_stub = {"database_path": context.random_file}
    

@when('Database is instantiated')
def step_impl(context):
    with mock.patch.object(aegis.database.Database, "new_database", mock.MagicMock(side_effect=fake_function)) as fake_new_db:
        context.aegisdb = aegis.database.Database(context.config_stub)
        assert fake_new_db.assert_called

@then('Database creates a new database file')
def step_impl(context):
    assert context.aegisdb.get() != None
    with mock.patch("json.dump", mock.MagicMock(fake_function)) as fake_json_dump:
        context.aegisdb.save()
        assert fake_json_dump.assert_called