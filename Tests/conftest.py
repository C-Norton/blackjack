# conftest.py

import pytest


@pytest.fixture
def generate_fake_card(mocker):
    def g(fake_suit, fake_value):
        m = mocker.Mock()
        m.suit = fake_suit
        m.value = fake_value
        m.__str__ = mocker.Mock(return_value=str(fake_value) + str(fake_suit))
        return m

    return g
