"""Test module for the AWS lambda function."""

import pytest

STANDARDS = [
    (['version'], '1.0'),
    (['response', 'outputSpeech', 'type'], 'PlainText'),
    (['response', 'card', 'type'], 'Simple'),
    (['response', 'reprompt', 'outputSpeech', 'type'], 'PlainText'),
]


@pytest.mark.parametrize('response, expected', STANDARDS)
def test_launch_standards(launch, result_to_dict, response, expected):
    """Test numerous output as expected are returned from launch of skill."""
    if len(response) == 1:
        result = result_to_dict[response[0]]
    elif len(response) == 3:
        result = result_to_dict[response[0]][response[1]][response[2]]
    elif len(response) == 4:
        result = result_to_dict[response[0]] \
         [response[1]][response[2]][response[3]]
    assert result == expected


def test_launch_session_attributes(launch, result_to_dict):
    """SessionAttributes should return empty from launch of skill."""
    assert result_to_dict['sessionAttributes'] == {}


def test_launch_card_content(launch, result_to_dict):
    """Welcome message should be returned from launch of skill."""
    content = result_to_dict['response']['card']['content']
    message = "Welcome to AIM messaging"
    assert content == message


def test_launch_reprompt_speech(launch, result_to_dict):
    """Welcome message should be returned on launch of skill."""
    text = result_to_dict['response']['reprompt']['outputSpeech']['text']
    speech = "Do you want to send or receive a message."
    assert text == speech


def test_launch_end_session(launch, result_to_dict):
    """End session should be 'False' when returned on launch of skill."""
    end_session = result_to_dict['response']['shouldEndSession']
    # speech = "Do you want to send or receive a message."
    assert not end_session


@pytest.mark.parametrize('response, expected', STANDARDS)
def test_establish_recipient_standards(
        launch, result_to_dict, response, expected):
    """Test several expected output are returned from EstablishRecipient."""
    if len(response) == 1:
        result = result_to_dict[response[0]]
    elif len(response) == 3:
        result = result_to_dict[response[0]][response[1]][response[2]]
    elif len(response) == 4:
        result = result_to_dict[response[0]] \
         [response[1]][response[2]][response[3]]
    assert result == expected


def test_establish_recipient_returns_receiver(establish_recipient,
                                              result_to_dict):
    """Test receiver_name is 'DummyName'."""
    assert 'DummyName' in result_to_dict['sessionAttributes']['receiver_name']


def test_establish_recipient_session_attributes(establish_recipient,
                                                result_to_dict):
    """Test that session attributes are not empty dict"""
    assert result_to_dict['sessionAttributes']


def test_establish_recipient_returns_output_speech(establish_recipient,
                                                   result_to_dict):
    """Test output speech for alexa is correct output."""
    expected_output = "OK, send a message to DummyName, right?"
    actual_output = result_to_dict['response']['outputSpeech']['text']
    assert expected_output == actual_output


def test_receive_message_returns_no_messages(receive_message,
                                             result_to_dict):
    """Test no message is returned when receiver has no message."""
    speech_output = result_to_dict['response']['outputSpeech']['text']
    expected_output = "There are no messages for dummyname. "
    assert speech_output == expected_output


