import json
import logging
import os
from datetime import datetime, timedelta

import boto3
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# for local testing
# KEY = os.environ.get("API_KEY")
# HOST = os.environ.get("API_HOST")

s3 = boto3.client("s3")


def flatten_helper(keys: list, data: dict) -> dict:
    """
    Flattens Dictionary
    """

    for key in keys:
        data[key] = {key + "_" + subkey: val for subkey, val in data[key].items()}
        data.update(data[key])
        del data[key]

    return data


def lambda_handler(event, context):
    url = "https://ai-weather-by-meteosource.p.rapidapi.com/time_machine"
    KEY = event["KEY"]
    HOST = event["HOST"]
    headers = {"X-RapidAPI-Key": KEY, "X-RapidAPI-Host": HOST}
    bucket = "forecast-flow-ingestion-main"
    current_date = datetime.now().date()
    filename = f"{current_date}_{current_date - timedelta(days=5)}_dataset"

    processed = []
    for i in range(5, 0, -1):
        date_in_iteration = current_date - timedelta(days=i)
        querystring = {
            "date": date_in_iteration,
            "place_id": "london",
            "units": "metric",
        }

        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()["data"]

        for info in data:
            processed.append(flatten_helper(["wind", "precipitation"], info))
    uploadstream = bytes(json.dumps(processed).encode("UTF-8"))
    s3.put_object(Bucket=bucket, Key=filename, Body=uploadstream)

    return response.status_code
