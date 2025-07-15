"""
FILENAME: test_game_edge_cases.py

AUTHOR: Enhanced Testing Suite
CREATED ON: 7/14/2025

Edge case tests for game.py logic, file I/O, and integration scenarios
"""

import collections
import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import mock_open

from Blackjack.game import Game, generate_deck
from Blackjack.player import Player, load_player, save_player
from Blackjack.result import Result
from Blackjack.move import Move
from Blackjack.suit import Suit
from Blackjack.value import Value


class TestGameEdgeCases:
    @pytest.fixture(scope="class")
    def class_setup(self, request):
        print(f"Setting up class: {request.cls.__name__}")
        yield
        print(f"Tearing down class: {request.cls.__name__}")

    @pytest.fixture
    def method_setup(self, request, mocker):
        print(f"Setting up method: {request.function.__name__}")
        self.fake_input = mocker.patch("builtins.input")
        self.fake_print = mocker.patch("builtins.print")
        self.deck = collections.deque()
        self.fake_player = mocker.Mock()
        self.fake_dealer_hand = mocker.Mock()
        self.fake_player_hand = mocker.Mock()
        self.fake_dealer = mocker.Mock()
        self.fake_dealer.hand = self.fake_dealer_hand
        self.fake_player.hand = self.fake_player_hand
        self.game = Game(self.fake_player, self.fake_dealer, self.deck)
        yield
        print(f"Tearing down method: {request.function.__name__}")

    # ==================== DECK EDGE CASES ====================

    def test_generate_deck_completeness(self, class_setup, method_setup):
        """Test that generated deck contains exactly 52 unique cards"""
        deck = generate_deck()
        assert len(deck) == 52

        # Check all combinations exist
        card_set = set()
        for card_obj in deck:
            card_tuple = (card_obj.suit, card_obj.value)
            assert card_tuple not in card_set, f"Duplicate card: {card_obj}"
            card_set.add(card_tuple)

        # Verify all 52 combinations are present
        assert len(card_set) == 52

    def test_empty_deck_during_deal(self, class_setup, method_setup, mocker):
        """Test behavior when deck runs out during deal"""
        # Create a deck with only 3 cards (need 4 for dealing)
        limited_deck = collections.deque([
            mocker.Mock(),
            mocker.Mock(),
            mocker.Mock()
        ])
        game_instance = Game(self.fake_player, self.fake_dealer, limited_deck)

        with pytest.raises(IndexError):
            game_instance.deal()

    def test_empty_deck_during_hit(self, class_setup, method_setup, mocker):
        """Test behavior when deck runs out during player hit"""
        self.fake_player_hand.get_total.return_value = 15
        self.fake_player.take_turn.side_effect = [Move.HIT]
        self.fake_player.has_busted.return_value = False

        # Empty deck should cause IndexError when player tries to hit
        with pytest.raises(IndexError):
            self.game.play_round()

    def test_single_card_deck(self, class_setup, method_setup, generate_fake_card):
        """Test game behavior with minimal deck"""
        single_card = generate_fake_card(Suit.SPADES, Value.ACE)
        single_deck = collections.deque([single_card])
        game_instance = Game(self.fake_player, self.fake_dealer, single_deck)

        with pytest.raises(IndexError):  # Should fail when trying to deal 4 cards
            game_instance.deal()

    # ==================== GAME EVALUATION EDGE CASES ====================

    def test_evaluate_both_blackjack_tie(self, class_setup, method_setup):
        """Test evaluation when both player and dealer have blackjack"""
        self.fake_player_hand.get_total.return_value = 21
        self.fake_dealer_hand.get_total.return_value = 21
        self.fake_player_hand.get_size.return_value = 2
        self.fake_dealer_hand.get_size.return_value = 2
        self.game.player.hand = self.fake_player_hand
        self.game.dealer.hand = self.fake_dealer_hand
        assert self.game.evaluate() == Result.PUSH

    def test_evaluate_both_bust_edge_case(self, class_setup, method_setup):
        """Test evaluation when both player and dealer bust (player loses)"""
        self.fake_player_hand.get_total.return_value = 22
        self.fake_dealer_hand.get_total.return_value = 23
        self.game.player.hand = self.fake_player_hand
        self.game.dealer.hand = self.fake_dealer_hand
        assert self.game.evaluate() == Result.DEFEAT  # Player busts first

    def test_evaluate_player_21_multiple_cards_dealer_blackjack(self, class_setup, method_setup):
        """Test when player has 21 with multiple cards, dealer has blackjack"""
        self.fake_player_hand.get_total.return_value = 21
        self.fake_dealer_hand.get_total.return_value = 21
        self.fake_player_hand.get_size.return_value = 5  # 21 with multiple cards
        self.fake_dealer_hand.get_size.return_value = 2  # Blackjack
        self.game.player.hand = self.fake_player_hand
        self.game.dealer.hand = self.fake_dealer_hand
        assert self.game.evaluate() == Result.DEFEAT

    def test_evaluate_maximum_possible_totals(self, class_setup, method_setup):
        """Test evaluation with maximum possible hand totals"""
        self.fake_player_hand.get_total.return_value = 20
        self.fake_dealer_hand.get_total.return_value = 21
        self.fake_player_hand.get_size.return_value = 3
        self.fake_dealer_hand.get_size.return_value = 3
        self.game.player.hand = self.fake_player_hand
        self.game.dealer.hand = self.fake_dealer_hand
        assert self.game.evaluate() == Result.DEFEAT

    # ==================== PLAY ROUND EDGE CASES ====================

    def test_play_round_player_double_down_bust(self, class_setup, method_setup):
        """Test play round when player doubles down and busts"""
        self.fake_player_hand.get_total.return_value = 25
        self.fake_player.take_turn.return_value = Move.DOUBLE_DOWN
        self.fake_player.has_busted.return_value = True

        assert self.game._can_player_move
        result = self.game.play_round()
        assert not result  # Game should end
        assert not self.game._can_player_move

    def test_play_round_dealer_immediate_21(self, class_setup, method_setup):
        """Test play round when dealer has immediate 21"""
        self.fake_player_hand.get_total.return_value = 20
        self.fake_player.take_turn.return_value = Move.STAND
        self.fake_dealer_hand.get_total.return_value = 21
        self.fake_dealer.take_turn.return_value = Move.STAND
        self.fake_player.has_busted.return_value = False
        self.fake_dealer.has_busted.return_value = False

        result = self.game.play_round()
        assert not result  # Game should end
        assert not self.game._can_player_move

    def test_play_round_multiple_hits_then_stand(self, class_setup, method_setup):
        """Test multiple round sequence ending in stand"""
        self.fake_player.take_turn.side_effect = [Move.HIT, Move.HIT, Move.STAND]
        self.fake_dealer.take_turn.side_effect = [Move.HIT, Move.HIT, Move.STAND]
        self.fake_player.has_busted.return_value = False
        self.fake_dealer.has_busted.return_value = False

        # First round - hit
        result1 = self.game.play_round()
        assert result1
        assert self.game._can_player_move

        # Second round - hit
        result2 = self.game.play_round()
        assert result2
        assert self.game._can_player_move

        # Third round - stand
        result3 = self.game.play_round()
        assert not result3
        assert not self.game._can_player_move

    # ==================== NEW HAND INTEGRATION EDGE CASES ====================

    def test_new_hand_player_immediate_blackjack(self, class_setup, method_setup, generate_fake_card):
        """Test new hand when player gets immediate blackjack"""
        # Set up deck for blackjack scenario
        fake_cards = [
            generate_fake_card(Suit.SPADES, Value.ACE),   # Player card 1
            generate_fake_card(Suit.HEARTS, Value.SEVEN), # Dealer card 1
            generate_fake_card(Suit.CLUBS, Value.KING),   # Player card 2
            generate_fake_card(Suit.DIAMONDS, Value.EIGHT) # Dealer card 2
        ]

        for fake_card in reversed(fake_cards):
            self.deck.append(fake_card)

        self.fake_player.ante.return_value = 50
        self.fake_player_hand.get_total.return_value = 21
        self.fake_dealer_hand.get_total.return_value = 15
        self.fake_player_hand.get_size.return_value = 2
        self.fake_dealer_hand.get_size.return_value = 2
        self.fake_player.take_turn.return_value = Move.STAND
        self.fake_dealer.take_turn.return_value = Move.STAND
        self.fake_player.has_busted.return_value = False
        self.fake_dealer.has_busted.return_value = False
        self.fake_player.bet = 50

        result, net_change = self.game.new_hand()
        assert result == Result.VICTORY
        assert net_change == 50

    def test_new_hand_dealer_immediate_blackjack(self, class_setup, method_setup, generate_fake_card):
        """Test new hand when dealer gets immediate blackjack"""
        fake_cards = [
            generate_fake_card(Suit.SPADES, Value.FIVE),  # Player card 1
            generate_fake_card(Suit.HEARTS, Value.ACE),   # Dealer card 1
            generate_fake_card(Suit.CLUBS, Value.SIX),    # Player card 2
            generate_fake_card(Suit.DIAMONDS, Value.KING) # Dealer card 2
        ]

        for fake_card in reversed(fake_cards):
            self.deck.append(fake_card)

        self.fake_player.ante.return_value = 50
        self.fake_player_hand.get_total.return_value = 11
        self.fake_dealer_hand.get_total.return_value = 21
        self.fake_player_hand.get_size.return_value = 2
        self.fake_dealer_hand.get_size.return_value = 2
        self.fake_player.take_turn.return_value = Move.STAND
        self.fake_dealer.take_turn.return_value = Move.STAND
        self.fake_player.has_busted.return_value = False
        self.fake_dealer.has_busted.return_value = False
        self.fake_player.bet = 50

        result, net_change = self.game.new_hand()
        assert result == Result.DEFEAT
        assert net_change == -50


class TestFileIOEdgeCases:
    @pytest.fixture(scope="class")
    def class_setup(self, request):
        print(f"Setting up class: {request.cls.__name__}")
        yield
        print(f"Tearing down class: {request.cls.__name__}")

    @pytest.fixture
    def method_setup(self, request):
        print(f"Setting up method: {request.function.__name__}")
        self.temp_dir = tempfile.mkdtemp()
        yield
        print(f"Tearing down method: {request.function.__name__}")
        # Clean up temp files
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    # ==================== FILE I/O EDGE CASES ====================

    def test_save_player_to_nonexistent_directory(self, class_setup, method_setup):
        """Test saving player to nonexistent directory"""
        player = Player.from_name_bankroll("Test Player", 100)
        nonexistent_path = Path(self.temp_dir) / "nonexistent" / "player.blackjack"

        # Should raise FileNotFoundError due to missing parent directory
        with pytest.raises(FileNotFoundError):
            save_player(player, nonexistent_path)

    def test_save_player_with_special_characters(self, class_setup, method_setup):
        """Test saving player with special characters in stats"""
        special_stats = {
            "name": "Player!@#$%^&*()",
            "bankroll": 100,
            "wins": 5,
            "losses": 3,
            "pushes": 2,
            "special_field": "unicode: 你好"
        }
        player = Player(special_stats)
        file_path = Path(self.temp_dir) / "special_player.blackjack"

        save_player(player, file_path)
        assert file_path.exists()

        loaded_player = load_player(file_path)
        assert loaded_player.stats == special_stats

    def test_load_player_corrupted_json(self, class_setup, method_setup):
        """Test loading player from corrupted JSON file"""
        file_path = Path(self.temp_dir) / "corrupted.blackjack"

        # Write invalid JSON
        with open(file_path, "w") as f:
            f.write("{ invalid json content }")

        with pytest.raises(json.JSONDecodeError):
            load_player(file_path)

    def test_load_player_empty_file(self, class_setup, method_setup):
        """Test loading player from empty file"""
        file_path = Path(self.temp_dir) / "empty.blackjack"

        # Create empty file
        file_path.touch()

        with pytest.raises(json.JSONDecodeError):
            load_player(file_path)

    def test_load_player_missing_required_fields(self, class_setup, method_setup):
        """Test loading player with missing required fields"""
        file_path = Path(self.temp_dir) / "incomplete.blackjack"

        # Save JSON with missing fields
        incomplete_stats = {"name": "Test"}  # Missing bankroll, wins, etc.
        with open(file_path, "w") as f:
            json.dump(incomplete_stats, f)

        player = load_player(file_path)
        # Should load but accessing missing fields might cause KeyError
        assert player.name == "Test"

        # This should raise KeyError due to missing bankroll
        with pytest.raises(KeyError):
            _ = player.bankroll

    def test_load_player_invalid_data_types(self, class_setup, method_setup):
        """Test loading player with invalid data types"""
        file_path = Path(self.temp_dir) / "invalid_types.blackjack"

        # Save JSON with wrong data types
        invalid_stats = {
            "name": 12345,  # Should be string
            "bankroll": "not_a_number",  # Should be int
            "wins": -1,  # Questionable but technically valid
            "losses": 3.5,  # Should be int
            "pushes": None  # Should be int
        }
        with open(file_path, "w") as f:
            json.dump(invalid_stats, f)

        player = load_player(file_path)
        assert player.stats == invalid_stats  # Data loads as-is

        # But operations might fail
        with pytest.raises(TypeError):
            _ = player.bankroll + 100  # Can't add int to string

    def test_save_load_player_very_large_bankroll(self, class_setup, method_setup):
        """Test save/load with very large bankroll values"""
        large_bankroll = 10**18  # Very large number
        player = Player.from_name_bankroll("Rich Player", large_bankroll)
        file_path = Path(self.temp_dir) / "rich_player.blackjack"

        save_player(player, file_path)
        loaded_player = load_player(file_path)

        assert loaded_player.bankroll == large_bankroll
        assert loaded_player == player

    def test_save_load_player_unicode_name(self, class_setup, method_setup):
        """Test save/load with unicode characters in name"""
        unicode_name = "玩家123🃏♠️♥️♦️♣️"
        player = Player.from_name_bankroll(unicode_name, 100)
        file_path = Path(self.temp_dir) / "unicode_player.blackjack"

        save_player(player, file_path)
        loaded_player = load_player(file_path)

        assert loaded_player.name == unicode_name
        assert loaded_player == player

    def test_concurrent_file_access_simulation(self, class_setup, method_setup, mocker):
        """Test behavior when file is being accessed concurrently"""
        player = Player.from_name_bankroll("Test Player", 100)
        file_path = Path(self.temp_dir) / "concurrent.blackjack"

        # Mock file operations to simulate permission error
        mock_file = mock_open()
        mock_file.side_effect = PermissionError("File is locked by another process")

        with mocker.patch("builtins.open", mock_file):
            with pytest.raises(PermissionError):
                save_player(player, file_path)

    def test_load_player_file_not_found(self, class_setup, method_setup):
        """Test loading player from non-existent file"""
        nonexistent_path = Path(self.temp_dir) / "nonexistent.blackjack"

        with pytest.raises(FileNotFoundError):
            load_player(nonexistent_path)

    def test_save_load_zero_stats_player(self, class_setup, method_setup):
        """Test save/load player with all zero stats"""
        zero_stats = {
            "name": "Zero Player",
            "bankroll": 0,
            "wins": 0,
            "losses": 0,
            "pushes": 0
        }
        player = Player(zero_stats)
        file_path = Path(self.temp_dir) / "zero_player.blackjack"

        save_player(player, file_path)
        loaded_player = load_player(file_path)

        assert loaded_player.stats == zero_stats
        assert loaded_player == player