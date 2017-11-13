def lambda_handler(event, context):
    # TODO implement
    if (event["session"]["application"]["applicationId"] !=
        "amzn1.ask.skill.ff117040-72fc-409a-a82f-cdba631d7f2d"):
        raise ValueError("Invalid Application ID")

    if event["session"]["new"]:
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])
    print(event)
    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])


def on_session_started(session_started_request, session):
    print("Starting new session.")

def on_launch(launch_request, session):
    return get_welcome_response()

def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    if intent_name == "SendMessage":
        return send_message(intent, session)
    elif intent_name == "ReceiveMessage":
        return receive_message(intent, session)
    elif intent_name == "PrepareMessage":
        return prepare_message(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return on_session_ended()
    else:
        raise ValueError("Invalid intent")

def prepare_message(intent, session):
    session_attributes = {}
    card_title = "AIM"
    speech_output = "OK! i sent the following message, {}".format(intent["slots"]["Message"]["value"])
    reprompt_text = ""
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def send_message(intent, session):
    session_attributes = {}
    card_title = "AIM"
    speech_output = "OK send a message to {} What is your message".format(intent["slots"]["Name"]["value"])
    reprompt_text = ""
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def receive_message(intent, session):
    session_attributes = {}
    card_title = "AIM"
    speech_output = "This is your message from {}".format(intent["slots"]["Name"]["value"])
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
