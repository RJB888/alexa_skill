"""Test module for the AWS lambda function."""

import pytest


def test_establish_recipient(establish_recipient_intent):
    """Test that the function will return the recipient value of 'Bob'."""
    assert 'Bob' in establish_recipient_intent['sessionAttributes']['recipient']