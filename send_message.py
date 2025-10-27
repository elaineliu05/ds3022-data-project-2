import os
import boto3
import time

url = "https://sqs.us-east-1.amazonaws.com/440848399208/dp2-submit"
sqs = boto3.client('sqs')

def send_solution(uvaid, phrase, platform):
    try:
        response = sqs.send_message(
            QueueUrl=url,
            MessageBody="data project 2 submission",
            MessageAttributes={
                'uvaid': {
                    'DataType': 'String',
                    'StringValue': uvaid
                },
                'phrase': {
                    'DataType': 'String',
                    'StringValue': phrase
                },
                'platform': {
                    'DataType': 'String',
                    'StringValue': platform
                }
            }
        )
        print(f"Response: {response}")

    except Exception as e:
        print(f"Error sending message: {e}")
        raise e
