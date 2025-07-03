import collections
import unittest
from unittest.mock import Mock
from unittest.mock import patch

import card
import dealer
import game
import hand
import player
from move import Move
from player import Player
from suit import Suit
from value import Value


class BlackJackTest(unittest.TestCase):

    @staticmethod
    def test_hand():
        my_hand = hand.Hand()

        # Set up mocks; we mock __str__ differently because it's a dunder (__) method,
        # meaning Python handles it differently
        fake_card1 = Mock()
        fake_card1.get_value.return_value = Value.ACE
        fake_card1.get_suit.return_value = Suit.CLUBS
        fake_card1.__str__ = Mock(return_value="A♣")

        fake_card2 = Mock()
        fake_card2.get_value.return_value = Value.QUEEN
        fake_card2.get_suit.return_value = Suit.SPADES
        fake_card2.__str__ = Mock(return_value="Q♠")

        fake_card3 = Mock()
        fake_card3.get_value.return_value = Value.ACE
        fake_card3.get_suit.return_value = Suit.DIAMONDS
        fake_card3.__str__ = Mock(return_value="A♦")

        fake_card4 = Mock()
        fake_card4.get_value.return_value = Value.SEVEN
        fake_card4.get_suit.return_value = Suit.HEARTS
        fake_card4.__str__ = Mock(return_value="7♥")

        # add cards and set assertions
        my_hand.add_card(fake_card1)
        assert my_hand.get_total() == 11
        assert my_hand.get_size() == 1

        my_hand.add_card(fake_card2)
        assert my_hand.get_total() == 21
        assert my_hand.get_size() == 2

        my_hand.add_card(fake_card3)
        assert my_hand.get_total() == 12
        assert my_hand.get_size() == 3

        my_hand.add_card(fake_card4)
        assert my_hand.get_total() == 19
        assert my_hand.get_size() == 4

        assert str(my_hand) == "A♣\nQ♠\nA♦\n7♥"

    @staticmethod
    def test_cards():
        card1 = card.Card(Suit.SPADES, Value.SEVEN)
        card2 = card.Card(Suit.CLUBS, Value.TEN)
        card3 = card.Card(Suit.DIAMONDS, Value.KING)
        card4 = card.Card(Suit.HEARTS, Value.ACE)

        # Stupid checks, but hey, just to be sure
        assert card1.get_value() == Value.SEVEN
        assert card1.get_suit() == Suit.SPADES
        assert card2.get_value() == Value.TEN
        assert card2.get_suit() == Suit.CLUBS
        assert card3.get_value() == Value.KING
        assert card3.get_suit() == Suit.DIAMONDS
        assert card4.get_value() == Value.ACE
        assert card4.get_suit() == Suit.HEARTS

        assert str(card1) == "7♠"
        assert str(card2) == "10♣"
        assert str(card3) == "K♦"
        assert str(card4) == "A♥"

        # The checks in this block are redundant, but this verifies
        # That the representation comes from __str__ and not __repr__
        assert card1.__str__() == "7♠"
        assert card2.__str__() == "10♣"
        assert card3.__str__() == "K♦"
        assert card4.__str__() == "A♥"

        card1.flip()
        assert card1.is_facedown() == True
        assert card1.__str__() == "##"
        assert str(card1) == "##"
        card1.flip()
        assert card1.__str__() == "7♠"
        assert str(card1) == "7♠"

    @staticmethod
    def test_dealer():
        """
        In order to test this properly, we need to inject a mock hand instance into the dealer
        Hand 1 will have a deck like the below

        TOP OF DECK
        "A♣"
        "Q♠"
        "A♦"
        "7♥"
        BOTTOM OF DECK

        Hand 2 will have a deck like the below
        TOP OF DECK
        "5♣"
        "Q♠"
        "A♦"
        "7♥"
        BOTTOM OF DECK

        there will be no player or game class, of course, so the dealer will take each card in order

        Game 1 should be, Hit-Hit-Stand
                          (11)(21)(21-blackjack)
        Game 2 should be, Hit-Hit-Hit-Hit
                          (5) (15)(16)(23)
        """

        deck = collections.deque()

        fake_card1 = Mock()
        fake_card1.get_value.return_value = Value.ACE
        fake_card1.get_suit.return_value = Suit.CLUBS
        fake_card1.__str__ = Mock(return_value="A♣")

        fake_card2 = Mock()
        fake_card2.get_value.return_value = Value.QUEEN
        fake_card2.get_suit.return_value = Suit.SPADES
        fake_card2.__str__ = Mock(return_value="Q♠")

        fake_card3 = Mock()
        fake_card3.get_value.return_value = Value.ACE
        fake_card3.get_suit.return_value = Suit.DIAMONDS
        fake_card3.__str__ = Mock(return_value="A♦")

        fake_card4 = Mock()
        fake_card4.get_value.return_value = Value.SEVEN
        fake_card4.get_suit.return_value = Suit.HEARTS
        fake_card4.__str__ = Mock(return_value="7♥")

        deck.append(fake_card1)
        deck.append(fake_card2)
        deck.append(fake_card3)
        deck.append(fake_card4)

        fake_hand = Mock()
        my_dealer = dealer.Dealer(fake_hand)

        fake_hand.get_total.return_value = 0
        fake_hand.get_size.return_value = 0
        move1 = my_dealer.take_turn(deck)
        assert len(deck) == 3
        assert deck[0] == fake_card2
        assert move1 == Move.HIT

        fake_hand.get_total.return_value = 11
        fake_hand.get_size.return_value = 1
        move2 = my_dealer.take_turn(deck)
        assert len(deck) == 2
        assert deck[0] == fake_card3
        assert move2 == Move.HIT

        fake_hand.get_total.return_value = 21
        fake_hand.get_size.return_value = 2
        move3 = my_dealer.take_turn(deck)
        assert len(deck) == 2
        assert deck[0] == fake_card3
        assert move3 == Move.STAND

        deck = collections.deque()

        fake_card5 = Mock()
        fake_card5.get_value.return_value = Value.ACE
        fake_card5.get_suit.return_value = Suit.CLUBS
        fake_card5.__str__ = Mock(return_value="5♣")

        fake_card6 = Mock()
        fake_card6.get_value.return_value = Value.QUEEN
        fake_card6.get_suit.return_value = Suit.SPADES
        fake_card6.__str__ = Mock(return_value="Q♠")

        fake_card7 = Mock()
        fake_card7.get_value.return_value = Value.ACE
        fake_card7.get_suit.return_value = Suit.DIAMONDS
        fake_card7.__str__ = Mock(return_value="A♦")

        fake_card8 = Mock()
        fake_card8.get_value.return_value = Value.SEVEN
        fake_card8.get_suit.return_value = Suit.HEARTS
        fake_card8.__str__ = Mock(return_value="7♥")

        deck.append(fake_card5)
        deck.append(fake_card6)
        deck.append(fake_card7)
        deck.append(fake_card8)

        my_dealer2 = dealer.Dealer(fake_hand)

        fake_hand.get_total.return_value = 0
        fake_hand.get_size.return_value = 0
        move1 = my_dealer2.take_turn(deck)

        assert len(deck) == 3
        assert deck[0] == fake_card6
        assert move1 == Move.HIT

        fake_hand.get_total.return_value = 5
        fake_hand.get_size.return_value = 1
        move2 = my_dealer2.take_turn(deck)
        assert len(deck) == 2
        assert deck[0] == fake_card7
        assert move2 == Move.HIT

        fake_hand.get_total.return_value = 15
        fake_hand.get_size.return_value = 2
        move3 = my_dealer2.take_turn(deck)
        assert len(deck) == 1
        assert deck[0] == fake_card8
        assert move3 == Move.HIT

        fake_hand.get_total.return_value = 16
        fake_hand.get_size.return_value = 3
        move4 = my_dealer2.take_turn(deck)
        assert len(deck) == 0
        assert move4 == Move.HIT

        fake_hand.get_total.return_value = 23
        fake_hand.get_size.return_value = 4
        move5 = my_dealer2.take_turn(deck)
        assert move5 == Move.STAND

    @staticmethod
    @patch("builtins.input")
    @patch("builtins.print")
    def test_game(fake_print, fake_input):
        # Generate deck
        deck = game.generate_deck()
        assert type(deck) is collections.deque
        assert len(deck) == 52
        assert type(deck.popleft()) is card.Card

        # New Player
        fake_input.side_effect = ["Player 1", "1000"]

        player1 = game.new_player()
        assert type(player1) is Player
        assert player1.get_name() == "Player 1"
        assert player1.get_bankroll() == 1000
        assert type(player1.get_stats()) is dict
        assert fake_input.call_count == 2
        fake_input.reset_mock()
        fake_input.side_effect = ["Player 2", "Bad Input", "2000"]
        player2 = game.new_player()
        assert type(player1) is Player
        assert player2.get_name() == "Player 2"
        assert player2.get_bankroll() == 2000
        assert type(player2.get_stats()) is dict
        assert fake_input.call_count == 3
        with (patch("game.new_hand", return_value="mocked") as new_hand, patch("game.new_player",
                                                                               return_value="mocked") as new_player, patch(
            "game.load_player", return_value="mocked") as load_player):
            fake_input.reset_mock()
            fake_print.reset_mock()
            fake_input.side_effect = ["1"]
            game.main_menu()

            assert fake_print.call_count == 5
            assert fake_input.call_count == 1
            assert new_hand.call_count == 1
            fake_print.reset_mock()
            fake_input.reset_mock()
            fake_input.side_effect = ["Foo", 2]
            game.main_menu()

            assert new_player.call_count == 1

            assert fake_print.call_count == 10
            assert fake_input.call_count == 2

            fake_print.reset_mock()
            fake_input.reset_mock()
            load_player.return_value = player.Player("Player 1", 1000)
            fake_input.side_effect = ["3", "Player 1"]
            game.main_menu()
            assert fake_print.call_count == 6
            assert fake_input.call_count == 2
            assert load_player.call_count == 1


if __name__ == '__main__':
    unittest.main()
