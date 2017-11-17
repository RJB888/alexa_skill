"""Pytest fixtures."""

import ast
import pytest
import subprocess
import boto3
# time.sleep() maybe needed if internet connection is slow
# import time


INTENTS = {
    "establish": "json/establish_recipient.json",
    "create": "json/create_message.json",
    "delete": "json/delete_from_db.json",
    "launch": "json/launch.json",
    "receive": "json/receive_message.json",
    "send": "json/send_message.json",
    "verify": "json/verify_message.json",
    "replay": "json/replay.json",
    "help": "json/help.json",
    "stop": "json/stop.json",
    "yes": "json/yes.json",
    "delete_no_message": "json/delete_no_message.json"
}


def aws_call(intents_file):
    """Run lambda function in aws from shell."""
    with open('returned.txt', 'w') as f:
        subprocess.call(["python-lambda-local",
                         "-l",
                         "lib/",
                         "-f",
                         "lambda_handler",
                         "-t",
                         "5",
                         "lambda_function.py",
                        intents_file],
                        stdout=f)
        # time.sleep(2)


@pytest.fixture
def establish_recipient():
    """Pass EstablishRecipient intents to run lambda function in aws."""
    aws_call(INTENTS['establish'])


@pytest.fixture
def receive_message():
    """Pass EstablishRecipient intents to run lambda function in aws."""
    aws_call(INTENTS['receive'])


@pytest.fixture
def launch():
    """Pass Launch intents to run lambda function in aws."""
    aws_call(INTENTS['launch'])


@pytest.fixture
def replay_message():
    """Pass replay intents to run lambda function in aws."""
    aws_call(INTENTS['replay'])


@pytest.fixture
def delete_message():
    """Pass delete intents to run lambda function in aws."""
    aws_call(INTENTS['delete'])


@pytest.fixture
def verify_message():
    """Pass verify intents to run lambda function in aws."""
    aws_call(INTENTS['verify'])


@pytest.fixture
def help_message():
    """Pass help intents to run lambda function in aws."""
    aws_call(INTENTS['help'])


@pytest.fixture
def stop_message():
    """Pass stop intents to run lambda function in aws."""
    aws_call(INTENTS['stop'])


@pytest.fixture
def delete_message_from_db():
    """Pass delete intents to run lambda function in aws."""
    aws_call(INTENTS['yes'])
    aws_call(INTENTS['delete'])
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('aim_messages')
    db_response = table.scan()
    return db_response


@pytest.fixture
def delete_no_message():
    """Pass delete intents to run lambda function in aws."""
    aws_call(INTENTS['delete_no_message'])
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('aim_messages')
    db_response = table.scan()
    return db_response


@pytest.fixture
def result_to_dict():
    """Get results from aws results that have been saved to file."""
    with open('returned.txt', 'r') as f:
        info = f.readlines()

    # delete file content
    with open('returned.txt', 'w'):
        pass

    result = ""
    for line in info:
        if line.startswith("{'version': '1.0'"):
            result = line
            break

    return ast.literal_eval(result)

