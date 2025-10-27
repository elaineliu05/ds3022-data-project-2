import os
import boto3
import time

#set queue URL, replace w/ computing id
queue_url = "https://sqs.us-east-1.amazonaws.com/440848399208/bpa2hu"
sqs = boto3.client('sqs')

#delete message after it has been received
def delete_message(queue_url, receipt_handle):
    try:
        response = sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        print(f"Response: {response}")
    #error handling
    except Exception as e:
        print(f"Error deleting message: {e}")
        raise e

#receive message from SQS queue
def receive_message(queue_url):
    try:
        response = sqs.receive_message(
            QueueUrl = queue_url,
            MessageSystemAttributeNames = ['All'],
            MessageAttributeNames = ['All'],
            MaxNumberOfMessages = 10,
            WaitTimeSeconds = 5,
            VisibilityTimeout = 60
        )
        if 'Messages' not in response:
            return None
        #first message received
        message = response['Messages'][0]
        #save receipt handle for deletion
        receipt_handle = message['ReceiptHandle']
        #save order_no for sorting
        order_no = int(message['MessageAttributes']['order_no']['StringValue'])
        #save word for concatenation
        word = message['MessageAttributes']['word']['StringValue']
        #delete after receiving
        delete_message(queue_url, receipt_handle)
        return (order_no, word)
    except Exception as e:
        print(f"Error receiving message: {e}")
        raise e

def get_messages():
    # try to get any messages with message-attributes from SQS queue:
    queue_url = "https://sqs.us-east-1.amazonaws.com/440848399208/bpa2hu"
    #save messages here
    msgs = []
    #for ordering later
    ordered_msgs = []
    try:
        #will always be 21 messages
        while len(msgs) < 21:
            #receive message
            msg = receive_message(queue_url)
            if msg:
                msgs.append(msg)
                #just for updating progress
                print(f"Collected {len(msgs)}/21 messages: {msg[1]}")
            else:
                print(f"{len(msgs)}/21 messages collected so far, waiting for delayed messages...")
                time.sleep(5)
        #sort by order_no
        ordered_msgs = sorted(msgs, key=lambda x: x[0]) 
        return ordered_msgs

    except Exception as e:
        print(f"Error getting message: {e}")
        raise e
    
def concatenate(messages):
    #join on words in order
    return " ".join([i[1] for i in messages]) 

if __name__ == "__main__":
    messages = get_messages()
    result = concatenate(messages)
    print(f"Final result: {result}")