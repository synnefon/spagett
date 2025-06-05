# for use in aws lambda function that backs an API

import json
from spagett_it import run_spagett


def lambda_handler(event, _):
    query_string = event["body"]
    noodles = run_spagett(query_string)

    return {"statusCode": 200 if noodles["success"] else 400, "body": noodles["body"]}
