from service.constants import DATASET_NAME, DATASET_PROVIDER 
from corva import Api, Logger, TaskEvent, task


@task
def lambda_handler(event: TaskEvent, api: Api):

# 3. Here is where you can declare your variables from the argument event: TaskEvent and start using Api and Logger functionalities. 

    # The task app can declare the following attributes from the TaskEvent: company_id: The company identifier; asset_id: The asset identifier.
    asset_id = event.asset_id
    company_id = event.company_id

    #The task app can declare variables from the properties {} object. 
    timestamp = event.properties["timestamp"]
    discounted_revenue = event.properties["discounted_revenue"]
    discounted_operating_costs = event.properties["discounted_operating_costs"]
    drilling_and_completions_costs = event.properties["drilling_and_completions_costs"]

# 4. Implement calculations and logic

    #Compute Net Present Value
    npv = discounted_revenue - discounted_operating_costs - drilling_and_completions_costs

    # Utilize the Logger functionality. The default log level is Logger.info. To use a different log level, the log level must be specified in the manifest.json file in the "settings.environment": {"LOG_LEVEL": "DEBUG"}. See the Logger documentation for more information.
    Logger.debug(f"{asset_id=} {company_id=} {timestamp=}")
    Logger.debug(f"{npv=}")

# 5. This is how to set up a body of a POST request to store the data.
    output = {
        "asset_id": asset_id,
        "company_id": company_id,
        "provider": DATASET_PROVIDER,
        "collection": DATASET_NAME,
        "data": {
            "discounted_revenue": discounted_revenue,
            "discounted_operating_costs": discounted_operating_costs,
            "drilling_and_completions_costs": drilling_and_completions_costs,
            "npv": npv
        },
        "version": 1,
        "timestamp": timestamp
    }

    # Utilize the Logger functionality.
    Logger.debug({f"{output=}"})

# 6. Save the newly calculated data in a custom dataset

    # Utilize the Api functionality. The data=outputs needs to be an an array because Corva's data is saved as an array of objects. Objects being records. See the Api documentation for more information.
    # Checking if any data is present and then seding a POST request to Corva Data API. Please note that data is always a list.
    if output:
        # if request fails, lambda will be reinvoked. so no exception handling
        api.post(
            f"/api/v1/data/{DATASET_PROVIDER}/{DATASET_NAME}/", data=[output],
        ).raise_for_status()
    return output
