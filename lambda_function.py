import boto3
import datetime
# from rx import Observable


def lambda_handler(event, context):
    """."""
    # show_table() #remove this
    # TODO implement
    if (event["session"]["application"]["applicationId"] !=
            "amzn1.ask.skill.ff117040-72fc-409a-a82f-cdba631d7f2d"):
        raise ValueError("Invalid Application ID")

    if event["session"]["new"]:
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])
    # print(event)
    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])


# this function adds an entry in the database
def show_table():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('aim_messages')
    table.put_item(Item={
        'id': 4,
        'receiver_name': 'Darren',
        'date': '11/13/2017',
        'message': 'Take off ya hoser!',
        'sender_name': 'John'
    })
    response = table.scan()
    print(sorted(response['Items'], key=lambda x: x['sender_name']))


def on_session_started(session_started_request, session):
    print("Starting new session.")


def on_launch(launch_request, session):
    return get_welcome_response()
    # this function launches the appropriate intent based on utterance


def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    if intent_name == "EstablishRecipient":
        return get_recipient(intent, session)
    elif intent_name == "ReceiveMessage":
        return receive_message(intent, session)
    elif intent_name == "VerifyMessage":
        return verification_of_message(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return on_session_ended()
    else:
        raise ValueError("Invalid intent")

"""
*****************************************************************************************************


"""


def get_recipient(intent, session):
    """Repeat function  the message that was saved to the database."""
    receiver_name = intent["slots"]["Name"]["value"]
    session_attributes = {"recipient": receiver_name}
    card_title = "AIM"
    speech_output = "OK send a message to {} What is your message".format(receiver_name)
    reprompt_text = ""
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def verification_of_message(intent, session):
    message_body = intent["slots"]["Message"]["value"]
    session["attributes"]["message_body"] = message_body
    card_title = "AIM"
    speech_output = "OK.  Your message to {} is, {}, right?".format(session["attributes"]["recipient"], message_body)
    # if not ok, prompt for repeat of message? re run get_recipient()?
    reprompt_text = ""
    # at some point add the message to the db
    save_msg_to_db(session)
    should_end_session = True
    return build_response(session["attributes"], build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def save_msg_to_db(session):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('aim_messages')
    db_response = table.scan()
    next_index = 1 + sorted(db_response["Items"], key=lambda x: x['id'])[-1]['id']
    print(sorted(db_response["Items"], key=lambda x: x['id'])[-1]['id'])
    table.put_item(Item={
        'id': next_index,
        'receiver_name': session["attributes"]["recipient"],
        'date': datetime.datetime.now().strftime('%m/%d/%y'),
        'message': session["attributes"]["message_body"],
        'sender_name': "RedCoat"
    })


def receive_message(intent, session):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('aim_messages')
    db_response = table.scan()
    session_attributes = {}
    sender_name = intent["slots"]["Name"]["value"].lower()
    message = []
    speech_output = ""
    for index, row in enumerate(db_response["Items"]):
        if row['sender_name'].lower() == sender_name:
            message.append(row["message"])
    card_title = "AIM"
    number_of_messages = len(message)
    if not number_of_messages:
        speech_output = "You don't have any messages from {}. ".format(sender_name)
    elif number_of_messages == 1:
        speech_output = "This is your message from {}. {} ".format(sender_name, message[0])
    else:
        speech_output = "Here are your messages from {}. ".format(sender_name)
        for index, value in enumerate(message):
            speech_output += "Message {}. {}. ".format(index + 1, value)
    reprompt_text = ""
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def on_session_ended():
    session_attributes = {}
    card_title = "AIM - Thanks"
    speech_output = "Thank you for using AIM.  See you next time!"
    reprompt_text = ""
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_welcome_response():
    session_attributes = {}
    card_title = "AIM"
    speech_output = "Welcome to AIM messaging"
    reprompt_text = "Do you want to send or receive a message."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }

