# prefect flow goes here
from prefect import flow, task
from receive_message import get_messages, concatenate
from send_message import send_solution
from populate import populate_queue

@task
def populate_sqs_queue():
    return populate_queue()

@task
def fetch_msgs():
    return get_messages()

@task
def concatenate_msgs(messages):
    return concatenate(messages)

@task
def send_msg(phrase):
    return send_solution("bpa2hu", phrase, "prefect")

@flow
def pipeline():
    populate_sqs_queue()
    messages = fetch_msgs()
    phrase = concatenate_msgs(messages)
    print("phrase:", phrase)
    send_msg(phrase)

if __name__ == "__main__":
    pipeline()