import json
import re
import ast
import boto3
import requests
import logging

from botocore.exceptions import ClientError
from sqs_handler import get_lotte_abroad_travel


def hello(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event,
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration


def sqs_hello(event, context):
    text = str(event["Records"][0]["body"])
    serailzer = {
        "request_id": 1234,
        "birthday": "19840526",
        "gender": "M",
        "start_date": "20200522",
        "end_date": "20200526",
    }
    if text == "lotte":
        result = get_lotte_abroad_travel(serailzer)
        print(result)

        return {"status_code": 200, "text": text}
    return {"status_code": 400, "text": "Nothing here"}


def call_sqs(event, context):

    sqs = boto3.client("sqs", endpoint_url="http://localhost:9324")
    queue_url = "http://0.0.0.0:9324/queue/MyTestQueue"
    try:
        response = sqs.send_message(
            QueueUrl=queue_url,
            DelaySeconds=10,
            MessageAttributes={
                "Title": {"DataType": "String", "StringValue": "The Whistler"},
                "Author": {"DataType": "String", "StringValue": "John Grisham"},
                "WeeksOn": {"DataType": "Number", "StringValue": "6"},
            },
            MessageBody="lotte",
        )
    except ClientError as e:
        logging.error(e)
        return None

    return response
