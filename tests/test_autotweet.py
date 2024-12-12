import pytest
from autotweet import generate_tweet, validate_secrets, health_check

def test_validate_secrets():
    # Mock environment variables
    with pytest.raises(ValueError):
        validate_secrets()

def test_generate_tweet():
    # Mock OpenAI response
    tweet = generate_tweet()
    assert len(tweet) <= 280

def test_health_check():
    status = health_check()
    assert status == True
