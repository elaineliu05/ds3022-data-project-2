import boto3

queue_url = "https://sqs.us-east-1.amazonaws.com/440848399208/bpa2hu"
sqs = boto3.client('sqs')

def get_queue_attributes(queue_url):
    try:
        response = sqs.get_queue_attributes(
            QueueUrl=queue_url,
            AttributeNames=['All']
        )
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error getting queue attributes: {e}")
        raise e

if __name__ == "__main__":
    get_queue_attributes(queue_url)