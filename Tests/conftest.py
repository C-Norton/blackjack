# conftest.py

import pytest


@pytest.fixture
def generate_fake_card(mocker):
    def g(fake_suit, fake_value):
        m = mocker.Mock()
        m.get_suit.return_value = fake_suit
        m.get_value.return_value = fake_value
        m.__str__ = mocker.Mock(return_value=str(fake_value) + str(fake_suit))
        return m

    return g
