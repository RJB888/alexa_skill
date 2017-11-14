"""Pytest fixtures."""

import pytest
import json


@pytest.fixture
def establish_recipient_intent():
    """Create a fixture to handle the intent establish recipient."""
    from lambda_function import lambda_handler
    event = {
        "session": {
            "new": True,
            "sessionId": "SessionId.cd539670-7ae2-4565-a917-909522a04557",
            "application": {
                "applicationId": "amzn1.ask.skill.ff117040-72fc-409a-a82f-cdba631d7f2d"
            },
            "attributes": {},
            "user": {
                "userId": "amzn1.ask.account.<userid>"
            }
        },
        "request": {
            "type": "IntentRequest",
            "requestId": "EdwRequestId.9fd1db80-46ca-4ff7-aaae-293e3517b8b2",
            "intent": {
                "name": "EstablishRecipient",
                    "slots": {
                        "Name": {
                            "name": "Name",
                            "value": "Bob"
                        }
                    }
            },
            "locale": "en-US",
            "timestamp": "2017-11-14T02:36:01Z"
        },
        "context": {
            "AudioPlayer": {
                "playerActivity": "IDLE"
            },
            "System": {
              "application": {
                "applicationId": "amzn1.ask.skill.ff117040-72fc-409a-a82f-cdba631d7f2d"
              },
              "user": {
                "userId": "amzn1.ask.account.<userid>"
              },
              "device": {
                "supportedInterfaces": {}
              }
            }
          },
          "version": "1.0"
        }
    context = ''
    return lambda_handler(event, context)