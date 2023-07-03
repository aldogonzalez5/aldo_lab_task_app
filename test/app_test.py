from corva import TaskEvent
from lambda_function import lambda_handler


def test_app(app_runner):
    event = TaskEvent(company_id=1, asset_id=1234, properties={'foo': "bar"})

    app_runner(lambda_handler, event=event)
