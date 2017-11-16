"""Functions to build out Alexa Intelligent Messaging Skill."""

import boto3
import datetime


def lambda_handler(event, context):
    """Parse out event type and the object, aka context."""
    if (event["session"]["application"]["applicationId"] !=
            "amzn1.ask.skill.ff117040-72fc-409a-a82f-cdba631d7f2d"):
        raise ValueError("Invalid Application ID")
    if event["session"]["new"]:
        on_session_started({"requestId": event["request"]["requestId"]},
                           event["session"])
    try:
        if event["request"]["type"] == "LaunchRequest":
            return on_launch(event["request"], event["session"])
        elif event["request"]["type"] == "IntentRequest":
            return on_intent(event["request"], event["session"])
        elif event["request"]["type"] == "SessionEndedRequest":
            return on_session_ended(event["request"], event["session"])
    except KeyError:
        return unsure_response(event["request"]["intent"], event["session"])


def on_session_started(session_started_request, session):
    """Handle any initiation on new session."""
    print("Starting new session.")


def on_launch(launch_request, session):
    """Handle the launch request function and the session object."""
    return get_welcome_response()


def on_intent(intent_request, session):
    """Conditional logic of series of Alexa skill intents."""
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]
    if intent_name == "EstablishRecipient":
        return get_recipient(intent, session)
    elif intent_name == "ReceiveMessage":
        return receive_message(intent, session)
    elif intent_name == "VerifyMessage":
        return verification_of_message(intent, session)
    elif intent_name == "DeleteMessage":
        return delete_message_by_sender(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return on_session_ended()
    elif intent_name == "AMAZON.YesIntent":
        return handle_verification(intent, session)
    elif intent_name == "AMAZON.NoIntent":
        return handle_nointent(intent, session)
    elif intent_name == "ReplayMessage":
        return replay_message(intent, session)
    else:
        raise ValueError("Invalid intent")


def handle_nointent(intent, session):
    """Handle reprompts if not repeated exactly."""
    if "message_body" in session["attributes"]:
        return re_prompt_message(intent, session)
    else:
        return re_prompt_name(intent, session)


def re_prompt_message(intent, session):
    """Reprompt for message when not repeated to user exactly."""
    session["attributes"]["message_body"] = ""
    session_attributes = session["attributes"]
    reprompt_text = ""
    card_title = "AIM"
    should_end_session = False
    speech_output = "OK, what is the message?"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def re_prompt_name(intent, session):
    """Reprompt for name if not repeated to user exactly."""
    session_attributes = {}
    reprompt_text = ""
    card_title = "AIM"
    should_end_session = False
    speech_output = "OK, who am I sending the message to?"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_verification(intent, session):
    """Handle verification of name or user when not repeated exactly."""
    if "message_body" in session["attributes"]:
        return save_msg_to_db(session)
    else:
        return what_is_your_message(intent, session)


def what_is_your_message(intent, session):
    """Repeat function the message that was saved to the database."""
    receiver_name = session["attributes"]["receiver_name"]
    session_attributes = {"receiver_name": receiver_name}
    card_title = "AIM"
    speech_output = "OK, what is your message to {}?".format(receiver_name)
    reprompt_text = ""
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_recipient(intent, session):
    """Repeat function  the message that was saved to the database."""
    receiver_name = intent["slots"]["ForName"]["value"]
    session_attributes = {"receiver_name": receiver_name}
    card_title = "AIM"
    speech_output = "OK, send a message to {}, right?".format(receiver_name)
    reprompt_text = ""
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def verification_of_message(intent, session):
    """Verify that message is properly formatted."""
    message_body = intent["slots"]["Message"]["value"]
    session["attributes"]["message_body"] = message_body
    card_title = "AIM"
    speech_output = "OK.  Your message to {} is, {}, right?".format(session["attributes"]["receiver_name"], message_body)
    reprompt_text = ""
    should_end_session = False
    return build_response(session["attributes"], build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def save_msg_to_db(session):
    """Save individual message to the database."""
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('aim_messages')
    db_response = table.scan()
    next_index = 1 + sorted(db_response["Items"], key=lambda x: x['id'])[-1]['id']
    print(sorted(db_response["Items"], key=lambda x: x['id'])[-1]['id'])
    table.put_item(Item={
        'id': next_index,
        'receiver_name': session["attributes"]["receiver_name"],
        'date': datetime.datetime.now().strftime('%m/%d/%y'),
        'message': session["attributes"]["message_body"],
        'sender_name': "RedCoat",  # do we want to include sender name?
        'heard': False
    })
    card_title = "AIM"
    speech_output = "OK.  Your message is saved."
    reprompt_text = ""
    should_end_session = True
    return build_response(session["attributes"], build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def receive_message(intent, session):
    """Return the messages based on receiver name."""
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('aim_messages')
    db_response = table.scan()
    session_attributes = {}
    receiver_name = intent["slots"]["ForName"]["value"].lower()
    message = []
    speech_output = ""
    for index, row in enumerate(db_response["Items"]):
        if row['receiver_name'].lower() == receiver_name and not row['heard']:
            session_attributes["receiver_name"] = row["receiver_name"]
            session_attributes["id"] = row["id"]
            message.append(row["message"])
            table.update_item(
                Key={
                    "id": row["id"],
                    "receiver_name": row["receiver_name"]
                },
                UpdateExpression="SET heard = :bool",
                ExpressionAttributeValues={
                    ":bool": "true"
                })
    card_title = "AIM"
    number_of_messages = len(message)
    if not number_of_messages:
        speech_output = "There are no messages for {}. ".format(receiver_name)
    elif number_of_messages == 1:
        speech_output = "Here is your message for {}. {} ".format(receiver_name, message[0])
    else:
        speech_output = "Here are the messages for {}. ".format(receiver_name)
        for index, value in enumerate(message):
            speech_output += "Message {}. {}. ".format(index + 1, value)
    reprompt_text = ""
    if not number_of_messages:
        should_end_session = True
    else:
        should_end_session = False

    session_attributes["message_body"] = speech_output
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def replay_message(intent, session):
    """Replay the last heard message or messages."""
    speech_output = session["attributes"]["message_body"]
    reprompt_text = ""
    card_title = "AIM"
    should_end_session = False
    return build_response(session["attributes"], build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def delete_message_by_sender(intent, session):
    """Delete message from database."""
    session_attributes = {}
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('aim_messages')
    db_response = table.scan()
    sender_name = intent["slots"]["FromName"]["value"]
    senders_last_message = sorted(db_response["Items"], key=lambda x: x['id'])
    card_title = "Delete Message"
    speech_output = "Your message has been deleted."
    reprompt_text = ""
    should_end_session = True
    for i in senders_last_message[::-1]:
        if sender_name == i["sender_name"]:
            table.delete_item(
                Key={
                    "id": i["id"],
                    "receiver_name": i["receiver_name"]
                })
            return build_response(session_attributes, build_speechlet_response(
                card_title, speech_output, reprompt_text, should_end_session))

    speech_output = "You haven't left a message."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def on_session_ended():
    """Close session, aka the skill is not active."""
    session_attributes = {}
    card_title = "AIM - Thanks"
    speech_output = "Thank you for using AIM.  See you next time!"
    reprompt_text = ""
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_welcome_response():
    """Introduce the skill's title and function."""
    session_attributes = {}
    card_title = "AIM"
    speech_output = "Welcome to AIM messaging"
    reprompt_text = "Do you want to send or receive a message."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_help_response():
    """Introduce the skill's functionality."""
    session_attributes = {}
    card_title = "AIM"
    speech_output = "Here's how to use AIM messaging. For example to send a \
                    message to Bob, say, send a message to Bob. And then \
                    follow the prompts. To receive a message, say, play \
                    messages for Bob. To replay a message, say, replay.\
                    To delete a message, say, delete a message from Bob."
    reprompt_text = "Do you want to send or receive a message."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def unsure_response(intent, session):
    """Will be returned to the user if Alexa was unsure about the intent."""
    session_attributes = {}
    card_title = "AIM - unsure response"
    speech_output = "I'm sorry, I didn't get that. Say help if you need it."
    reprompt_text = "Do you want to send or receive a message."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    """Build custom object to be returned and sent to Alexa."""
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
    """Return any data to persist throughout the session."""
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }
