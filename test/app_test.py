import json
import os

from corva import TaskEvent
from lambda_function import lambda_handler
from service.constants import DATASET_PROVIDER, DATASET_NAME

TEST_REQUESTS_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'requests')

class TestTakApp:
    '''
    Test class
    '''
    def test_app(self, app_runner, requests_mock):
        '''
        Test function
        '''
        request_file = os.path.join(TEST_REQUESTS_PATH, "post_request_sample.json")
        with open(request_file, encoding="utf8") as raw_request:
            request_event = json.load(raw_request)
        asset_id = request_event["task"]["asset_id"]
        request_properties = request_event["task"]["properties"]
        event = TaskEvent(company_id=1, asset_id=asset_id, properties=request_properties)


        discounted_revenue = request_event["task"]["properties"]["discounted_revenue"]
        discounted_operating_costs = request_event["task"]["properties"]["discounted_operating_costs"]
        drilling_and_completions_costs = request_event["task"]["properties"]["drilling_and_completions_costs"]
        npv = discounted_revenue - discounted_operating_costs - drilling_and_completions_costs

        requests_mock.post(f"https://data.localhost.ai/api/v1/data/{DATASET_PROVIDER}/{DATASET_NAME}/")
        output = app_runner(lambda_handler, event=event)
        assert npv == output["data"]["npv"]