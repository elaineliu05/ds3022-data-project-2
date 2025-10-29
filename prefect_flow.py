# prefect flow goes here
from prefect import flow, task
from prefect.logging import get_run_logger
from receive_message import get_messages, concatenate
from send_message import send_solution
from populate import populate_queue


@task
def populate_sqs_queue():
    logger = get_run_logger()
    logger.info("Populating SQS queue with messages")
    return populate_queue()

@task
def fetch_msgs():
    logger = get_run_logger()
    logger.info("Fetching messages from SQS queue")
    return get_messages()

@task
def concatenate_msgs(messages):
    logger = get_run_logger()
    logger.info("Concatenating messages")
    return concatenate(messages)

@task
def send_msg(phrase):
    logger = get_run_logger()
    logger.info("Sending concatenated phrase as solution")
    return send_solution("bpa2hu", phrase, "prefect")

@flow
def pipeline():
    logger = get_run_logger()
    logger.info("Starting Prefect pipeline flow")
    populate_sqs_queue()
    messages = fetch_msgs()
    phrase = concatenate_msgs(messages)
    print("phrase:", phrase)
    send_msg(phrase)

if __name__ == "__main__":
    pipeline()