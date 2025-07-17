"""
FILENAME: test_hand_edge_cases.py

AUTHOR: Enhanced Testing Suite
CREATED ON: 7/14/2025

Edge case tests for hand.py module, focusing on ace handling through public interface
"""

import pytest
from Blackjack import hand, card
from Blackjack.suit import Suit
from Blackjack.value import Value


class TestHandEdgeCases:
    @pytest.fixture(scope="class")
    def class_setup(self, request):
        print(f"Setting up class: {request.cls.__name__}")
        yield
        print(f"Tearing down class: {request.cls.__name__}")

    @pytest.fixture
    def method_setup(self, request):
        print(f"Setting up method: {request.function.__name__}")
        self.my_hand = hand.Hand()
        yield
        print(f"Tearing down method: {request.function.__name__}")

    # ==================== ACE BEHAVIOR TESTING THROUGH PUBLIC INTERFACE ====================

    def test_single_ace_optimal_value(self, class_setup, method_setup):
        """Test that single ace is valued at 11 when optimal"""
        self.my_hand.add_card(card.Card(Suit.SPADES, Value.ACE))
        assert self.my_hand.get_total() == 11
        assert self.my_hand.get_size() == 1

    def test_ace_with_ten_blackjack(self, class_setup, method_setup):
        """Test ace with ten-value card creates 21"""
        self.my_hand.add_card(card.Card(Suit.SPADES, Value.ACE))
        self.my_hand.add_card(card.Card(Suit.HEARTS, Value.KING))
        assert self.my_hand.get_total() == 21
        assert self.my_hand.get_size() == 2

    def test_ace_with_nine_soft_twenty(self, class_setup, method_setup):
        """Test ace with 9 creates soft 20"""
        self.my_hand.add_card(card.Card(Suit.SPADES, Value.ACE))
        self.my_hand.add_card(card.Card(Suit.HEARTS, Value.NINE))
        assert self.my_hand.get_total() == 20
        assert self.my_hand.get_size() == 2

    def test_ace_forces_low_value_to_avoid_bust(self, class_setup, method_setup):
        """Test ace becomes 1 when 11 would cause bust"""
        self.my_hand.add_card(card.Card(Suit.SPADES, Value.KING))  # 10
        self.my_hand.add_card(card.Card(Suit.HEARTS, Value.EIGHT))  # 18
        self.my_hand.add_card(card.Card(Suit.CLUBS, Value.ACE))  # 19 (ace as 1)
        assert self.my_hand.get_total() == 19
        assert self.my_hand.get_size() == 3

    # ==================== MULTIPLE ACES BEHAVIOR ====================

    def test_two_aces_one_high_one_low(self, class_setup, method_setup):
        """Test two aces: one valued at 11, one at 1"""
        self.my_hand.add_card(card.Card(Suit.SPADES, Value.ACE))
        self.my_hand.add_card(card.Card(Suit.HEARTS, Value.ACE))
        assert self.my_hand.get_total() == 12  # 11 + 1
        assert self.my_hand.get_size() == 2

    def test_three_aces_optimal_distribution(self, class_setup, method_setup):
        """Test three aces: one at 11, two at 1"""
        self.my_hand.add_card(card.Card(Suit.SPADES, Value.ACE))
        self.my_hand.add_card(card.Card(Suit.HEARTS, Value.ACE))
        self.my_hand.add_card(card.Card(Suit.DIAMONDS, Value.ACE))
        assert self.my_hand.get_total() == 13  # 11 + 1 + 1
        assert self.my_hand.get_size() == 3

    def test_four_aces_all_low_value(self, class_setup, method_setup):
        """Test four aces: one at 11, three at 1"""
        for suit in [Suit.SPADES, Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS]:
            self.my_hand.add_card(card.Card(suit, Value.ACE))
        assert self.my_hand.get_total() == 14  # 11 + 1 + 1 + 1
        assert self.my_hand.get_size() == 4

    def test_five_aces_theoretical_maximum(self, class_setup, method_setup):
        """Test theoretical scenario with five aces (using repeated suits)"""
        # Add 5 aces (some repeated suits for testing)
        for i in range(5):
            suit = [Suit.SPADES, Suit.HEARTS, Suit.DIAMONDS, Suit.CLUBS, Suit.SPADES][i]
            self.my_hand.add_card(card.Card(suit, Value.ACE))
        assert self.my_hand.get_total() == 15  # 11 + 1 + 1 + 1 + 1
        assert self.my_hand.get_size() == 5

    # ==================== ACE VALUE TRANSITIONS ====================

    def test_soft_to_hard_with_added_card(self, class_setup, method_setup):
        """Test soft hand becoming hard when card added"""
        # Start with soft 16 (A, 5)
        self.my_hand.add_card(card.Card(Suit.SPADES, Value.ACE))  # 11
        self.my_hand.add_card(card.Card(Suit.HEARTS, Value.FIVE))  # 16 (soft)
        assert self.my_hand.get_total() == 16

        # Add 8, should force ace to 1 (total 14, not 24)
        self.my_hand.add_card(card.Card(Suit.CLUBS, Value.EIGHT))  # 14 (ace now 1)
        assert self.my_hand.get_total() == 14
        assert self.my_hand.get_size() == 3

    def test_multiple_aces_transition_scenario(self, class_setup, method_setup):
        """Test complex scenario with multiple aces adjusting values"""
        # Start with two aces (A, A = 12)
        self.my_hand.add_card(card.Card(Suit.SPADES, Value.ACE))  # 11
        self.my_hand.add_card(card.Card(Suit.HEARTS, Value.ACE))  # 12 (11+1)
        assert self.my_hand.get_total() == 12

        # Add 9 for 21 (A=11, A=1, 9=9)
        self.my_hand.add_card(card.Card(Suit.CLUBS, Value.NINE))  # 21
        assert self.my_hand.get_total() == 21

        # Add another card to see aces adjust
        self.my_hand.add_card(
            card.Card(Suit.DIAMONDS, Value.THREE)
        )  # 15 (A=1, A=1, 9=9, 3=3)
        assert self.my_hand.get_total() == 14
        assert self.my_hand.get_size() == 4

    def test_ace_transition_boundary_at_21(self, class_setup, method_setup):
        """Test ace behavior exactly at 21 boundary"""
        # Build to exactly 21 with ace adjustment
        self.my_hand.add_card(card.Card(Suit.SPADES, Value.ACE))  # 11
        self.my_hand.add_card(card.Card(Suit.HEARTS, Value.FIVE))  # 16
        self.my_hand.add_card(card.Card(Suit.CLUBS, Value.FIVE))  # 21 (ace stays 11)
        assert self.my_hand.get_total() == 21
        assert self.my_hand.get_size() == 3

    def test_ace_transition_over_21_boundary(self, class_setup, method_setup):
        """Test ace adjusts when going over 21"""
        self.my_hand.add_card(card.Card(Suit.SPADES, Value.ACE))  # 11
        self.my_hand.add_card(card.Card(Suit.HEARTS, Value.FIVE))  # 16
        self.my_hand.add_card(card.Card(Suit.CLUBS, Value.SIX))  # 12 (ace becomes 1)
        assert self.my_hand.get_total() == 12  # 1 + 5 + 6
        assert self.my_hand.get_size() == 3

    # ==================== ACES WITH FACE CARDS ====================

    def test_ace_with_multiple_face_cards(self, class_setup, method_setup):
        """Test ace behavior with multiple ten-value cards"""
        self.my_hand.add_card(card.Card(Suit.SPADES, Value.KING))  # 10
        self.my_hand.add_card(card.Card(Suit.HEARTS, Value.QUEEN))  # 20
        self.my_hand.add_card(card.Card(Suit.CLUBS, Value.ACE))  # 21 (ace as 1)
        assert self.my_hand.get_total() == 21
        assert self.my_hand.get_size() == 3

    def test_multiple_aces_with_face_card(self, class_setup, method_setup):
        """Test multiple aces with a face card"""
        self.my_hand.add_card(card.Card(Suit.SPADES, Value.ACE))  # 11
        self.my_hand.add_card(card.Card(Suit.HEARTS, Value.ACE))  # 12 (11+1)
        self.my_hand.add_card(card.Card(Suit.CLUBS, Value.KING))  # 12 (1+1+10)
        assert self.my_hand.get_total() == 12
        assert self.my_hand.get_size() == 3

    def test_face_cards_then_multiple_aces(self, class_setup, method_setup):
        """Test adding multiple aces to existing face cards"""
        self.my_hand.add_card(card.Card(Suit.SPADES, Value.JACK))  # 10
        assert self.my_hand.get_total() == 10

        self.my_hand.add_card(card.Card(Suit.HEARTS, Value.ACE))  # 21 (ace as 11)
        assert self.my_hand.get_total() == 21

        self.my_hand.add_card(card.Card(Suit.CLUBS, Value.ACE))  # 12 (both aces as 1)
        assert self.my_hand.get_total() == 12
        assert self.my_hand.get_size() == 3

    # ==================== PROGRESSIVE HAND BUILDING ====================

    def test_progressive_ace_hand_building(self, class_setup, method_setup):
        """Test building a hand progressively and watching ace values adjust"""
        # Step 1: Single ace
        self.my_hand.add_card(card.Card(Suit.SPADES, Value.ACE))
        assert self.my_hand.get_total() == 11

        # Step 2: Add small card
        self.my_hand.add_card(card.Card(Suit.HEARTS, Value.THREE))
        assert self.my_hand.get_total() == 14  # 11 + 3

        # Step 3: Add another small card
        self.my_hand.add_card(card.Card(Suit.CLUBS, Value.FOUR))
        assert self.my_hand.get_total() == 18  # 11 + 3 + 4

        # Step 4: Add card that forces ace adjustment
        self.my_hand.add_card(card.Card(Suit.DIAMONDS, Value.FIVE))
        assert self.my_hand.get_total() == 13  # 1 + 3 + 4 + 5 (ace adjusted)
        assert self.my_hand.get_size() == 4

    def test_ace_rich_hand_progressive_building(self, class_setup, method_setup):
        """Test building hand with many aces progressively"""
        # Add aces one by one and verify totals
        self.my_hand.add_card(card.Card(Suit.SPADES, Value.ACE))
        assert self.my_hand.get_total() == 11  # A(11)

        self.my_hand.add_card(card.Card(Suit.HEARTS, Value.ACE))
        assert self.my_hand.get_total() == 12  # A(11) + A(1)

        self.my_hand.add_card(card.Card(Suit.CLUBS, Value.ACE))
        assert self.my_hand.get_total() == 13  # A(11) + A(1) + A(1)

        self.my_hand.add_card(card.Card(Suit.DIAMONDS, Value.ACE))
        assert self.my_hand.get_total() == 14  # A(11) + A(1) + A(1) + A(1)

        # Add a ten, should force all aces to 1
        self.my_hand.add_card(card.Card(Suit.SPADES, Value.TEN))
        assert self.my_hand.get_total() == 14  # A(1) + A(1) + A(1) + A(1) + 10
        assert self.my_hand.get_size() == 5

    # ==================== BOUNDARY CONDITIONS ====================

    def test_exactly_21_with_ace_optimization(self, class_setup, method_setup):
        """Test hands that total exactly 21 with optimal ace usage"""
        # Ace + 10 = 21 (blackjack)
        self.my_hand.add_card(card.Card(Suit.SPADES, Value.ACE))
        self.my_hand.add_card(card.Card(Suit.HEARTS, Value.TEN))
        assert self.my_hand.get_total() == 21

    def test_exactly_21_with_ace_as_one(self, class_setup, method_setup):
        """Test hand totaling 21 with ace forced to value 1"""
        self.my_hand.add_card(card.Card(Suit.SPADES, Value.FIVE))
        self.my_hand.add_card(card.Card(Suit.HEARTS, Value.FIVE))
        self.my_hand.add_card(card.Card(Suit.CLUBS, Value.FIVE))
        self.my_hand.add_card(card.Card(Suit.DIAMONDS, Value.FIVE))  # 20
        self.my_hand.add_card(card.Card(Suit.SPADES, Value.ACE))  # 21 (ace as 1)
        assert self.my_hand.get_total() == 21
        assert self.my_hand.get_size() == 5

    def test_bust_avoidance_with_aces(self, class_setup, method_setup):
        """Test that aces adjust to avoid busting when possible"""
        self.my_hand.add_card(card.Card(Suit.SPADES, Value.ACE))  # 11
        self.my_hand.add_card(card.Card(Suit.HEARTS, Value.NINE))  # 20
        self.my_hand.add_card(card.Card(Suit.CLUBS, Value.FIVE))  # 15 (ace becomes 1)
        assert self.my_hand.get_total() == 15  # Avoided bust
        assert self.my_hand.get_size() == 3

    def test_unavoidable_bust_with_aces(self, class_setup, method_setup):
        """Test bust scenario even with ace adjustment"""
        # Build hand that busts even with aces as 1s
        self.my_hand.add_card(card.Card(Suit.SPADES, Value.ACE))  # 1
        self.my_hand.add_card(card.Card(Suit.HEARTS, Value.TEN))  # 11
        self.my_hand.add_card(card.Card(Suit.CLUBS, Value.TEN))  # 21
        self.my_hand.add_card(card.Card(Suit.DIAMONDS, Value.TWO))  # 23 (bust)
        assert self.my_hand.get_total() == 23  # Bust unavoidable
        assert self.my_hand.get_size() == 4

    # ==================== HAND REPRESENTATION WITH ACES ====================

    def test_hand_string_with_aces(self, class_setup, method_setup):
        """Test string representation includes aces properly"""
        self.my_hand.add_card(card.Card(Suit.SPADES, Value.ACE))
        self.my_hand.add_card(card.Card(Suit.HEARTS, Value.KING))

        hand_str = str(self.my_hand)
        assert "A♠" in hand_str
        assert "K♥" in hand_str
        # Should show newest card first due to deque.appendleft
        assert hand_str == "K♥\nA♠"

    def test_hand_indexing_with_aces(self, class_setup, method_setup):
        """Test hand indexing works correctly with aces"""
        ace_card = card.Card(Suit.SPADES, Value.ACE)
        king_card = card.Card(Suit.HEARTS, Value.KING)

        self.my_hand.add_card(ace_card)
        self.my_hand.add_card(king_card)

        # Should be able to access cards by index
        assert self.my_hand[0] == king_card  # Newest first
        assert self.my_hand[1] == ace_card  # Oldest last
        assert self.my_hand.get_size() == 2

    # ==================== EDGE CASE COMBINATIONS ====================

    def test_all_aces_hand(self, class_setup, method_setup):
        """Test hand with only aces of different quantities"""
        # Test with varying numbers of aces
        test_cases = [
            (1, 11),  # 1 ace = 11
            (2, 12),  # 2 aces = 11 + 1
            (3, 13),  # 3 aces = 11 + 1 + 1
            (4, 14),  # 4 aces = 11 + 1 + 1 + 1
        ]

        for num_aces, expected_total in test_cases:
            test_hand = hand.Hand()
            for i in range(num_aces):
                suit = [Suit.SPADES, Suit.HEARTS, Suit.CLUBS, Suit.DIAMONDS][i % 4]
                test_hand.add_card(card.Card(suit, Value.ACE))

            assert test_hand.get_total() == expected_total
            assert test_hand.get_size() == num_aces

    def test_maximum_reasonable_hand_with_aces(self, class_setup, method_setup):
        """Test reasonably maximum hand size with aces"""
        # Build hand: A, A, A, A, 2, 2, 2 = 11 + 1 + 1 + 1 + 2 + 2 + 2 = 20
        for _ in range(4):
            self.my_hand.add_card(card.Card(Suit.SPADES, Value.ACE))
        for _ in range(3):
            self.my_hand.add_card(card.Card(Suit.HEARTS, Value.TWO))

        assert self.my_hand.get_total() == 20  # 11 + 1 + 1 + 1 + 2 + 2 + 2
        assert self.my_hand.get_size() == 7

    def test_empty_hand_total(self, class_setup, method_setup):
        """Test empty hand returns zero total"""
        assert self.my_hand.get_total() == 0
        assert self.my_hand.get_size() == 0
        assert str(self.my_hand) == ""
