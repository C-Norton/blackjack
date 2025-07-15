"""
FILENAME: test_parameterized_exceptions.py

AUTHOR: Enhanced Testing Suite
CREATED ON: 7/14/2025

Comprehensive parameterized tests and exception handling edge cases
"""

import collections
import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock

from Blackjack.player import Player, OutOfMoneyException, save_player, load_player
from Blackjack.move import Move
from Blackjack.result import Result


class TestParameterizedInputs:
    """Comprehensive parameterized testing for all input scenarios"""

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
        yield
        print(f"Tearing down method: {request.function.__name__}")

    # ==================== COMPREHENSIVE ANTE INPUT TESTING ====================

    @pytest.mark.parametrize("invalid_input,description", [
        ("", "empty string"),
        ("   ", "whitespace only"),
        ("abc", "alphabetic text"),
        ("123abc", "mixed alphanumeric"),
        ("!@#$%", "special characters"),
        ("-1", "negative number"),
        ("-100", "large negative"),
        ("0", "zero"),
        ("0.0", "zero float"),
        ("1.5", "decimal number"),
        ("1,000", "comma-separated number"),
        ("$100", "currency symbol"),
        ("100$", "trailing currency"),
        ("one hundred", "written number"),
        ("1e2", "scientific notation"),
        ("infinity", "infinity string"),
        ("NaN", "not a number"),
        ("\n", "newline character"),
        ("\t", "tab character"),
        ("　", "unicode whitespace"),
        ("١٠٠", "arabic numerals"),
        ("100.00", "decimal with zeros"),
        ("100.", "trailing decimal"),
        (".100", "leading decimal"),
        ("++100", "double positive"),
        ("--100", "double negative"),
        ("1 0 0", "spaced digits"),
        ("hundred", "word number"),
        ("1st", "ordinal number"),
        ("0x64", "hexadecimal"),
        ("0b1100100", "binary"),
        ("100j", "complex number"),
    ])
    def test_ante_comprehensive_invalid_inputs(self, invalid_input, description, class_setup, method_setup):
        """Test ante with comprehensive set of invalid inputs"""
        player = Player.from_name_bankroll("Test Player", 100)
        self.fake_input.side_effect = [invalid_input, "50"]

        player.ante()

        assert player.bet == 50
        assert self.fake_input.call_count == 2

    @pytest.mark.parametrize("bankroll,bet_amount,should_succeed", [
        (100, 1, True),      # minimum valid bet
        (100, 50, True),     # half bankroll
        (100, 100, True),    # full bankroll
        (100, 101, False),   # over bankroll
        (1, 1, True),        # minimum bankroll, minimum bet
        (1000000, 999999, True),  # large amounts
        (5, 3, True),        # odd numbers
        (10, 5, True),       # even numbers
    ])
    def test_ante_boundary_values(self, bankroll, bet_amount, should_succeed, class_setup, method_setup):
        """Test ante with various bankroll and bet combinations"""
        player = Player.from_name_bankroll("Test Player", bankroll)

        if should_succeed:
            self.fake_input.return_value = str(bet_amount)
            player.ante()
            assert player.bet == bet_amount
        else:
            self.fake_input.side_effect = [str(bet_amount), "1"]  # fallback to valid bet
            player.ante()
            assert player.bet == 1  # Should fallback to valid amount

    # ==================== COMPREHENSIVE MOVE INPUT TESTING ====================

    @pytest.mark.parametrize("move_input,expected_calls,expected_move", [
        # Valid hit variations
        ("hit", 1, Move.HIT),
        ("HIT", 1, Move.HIT),
        ("Hit", 1, Move.HIT),
        ("  hit  ", 1, Move.HIT),
        ("\thit\n", 1, Move.HIT),

        # Valid stand variations
        ("stand", 1, Move.STAND),
        ("STAND", 1, Move.STAND),
        ("Stand", 1, Move.STAND),
        ("  stand  ", 1, Move.STAND),

        # Valid double down variations
        ("double down", 1, Move.DOUBLE_DOWN),
        ("DOUBLE DOWN", 1, Move.DOUBLE_DOWN),
        ("Double Down", 1, Move.DOUBLE_DOWN),
        ("  double down  ", 1, Move.DOUBLE_DOWN),
    ])
    def test_take_turn_valid_inputs(self, move_input, expected_calls, expected_move, class_setup, method_setup):
        """Test take_turn with all valid input variations"""
        player = Player.from_name_bankroll("Test Player", 100)
        player.hand = Mock()
        deck = collections.deque([Mock()])

        self.fake_input.return_value = move_input

        result = player.take_turn(deck)

        assert result == expected_move
        assert self.fake_input.call_count == expected_calls

    @pytest.mark.parametrize("invalid_input,description", [
        ("h", "single letter"),
        ("s", "single letter"),
        ("d", "single letter"),
        ("hi", "partial word"),
        ("sta", "partial word"),
        ("double", "incomplete phrase"),
        ("down", "incomplete phrase"),
        ("hit me", "extra words"),
        ("please hit", "extra words"),
        ("stand up", "extra words"),
        ("fold", "poker term"),
        ("call", "poker term"),
        ("raise", "poker term"),
        ("quit", "quit command"),
        ("exit", "exit command"),
        ("help", "help command"),
        ("?", "question mark"),
        ("1", "number"),
        ("0", "zero"),
        ("true", "boolean"),
        ("false", "boolean"),
        ("yes", "yes/no"),
        ("no", "yes/no"),
        ("", "empty string"),
        ("   ", "whitespace"),
        ("　", "unicode whitespace"),
        ("\n", "newline"),
        ("\t", "tab"),
        ("hit\nstand", "multi-line"),
        ("HIT STAND", "multiple commands"),
        ("hit;stand", "semicolon separated"),
        ("hit,stand", "comma separated"),
        ("hit/stand", "slash separated"),
        ("hit|stand", "pipe separated"),
        ("دؐouble down", "unicode characters"),
    ])
    def test_take_turn_comprehensive_invalid_inputs(self, invalid_input, description, class_setup, method_setup):
        """Test take_turn with comprehensive set of invalid inputs"""
        player = Player.from_name_bankroll("Test Player", 100)
        player.hand = Mock()
        deck = collections.deque([Mock()])

        self.fake_input.side_effect = [invalid_input, "hit"]

        result = player.take_turn(deck)

        assert result == Move.HIT
        assert self.fake_input.call_count == 2

    # ==================== COMPREHENSIVE BANKROLL TESTING ====================

    @pytest.mark.parametrize("initial_bankroll,change,expected_result,expected_final", [
        (100, 50, True, 150),        # positive change
        (100, 0, True, 100),         # no change
        (100, -50, True, 50),        # negative change within limit
        (100, -100, True, 0),        # negative change to exactly zero
        (100, -101, False, 100),     # negative change exceeding limit
        (0, 50, True, 50),           # from zero to positive
        (0, 0, True, 0),             # zero to zero
        (0, -1, False, 0),           # can't go negative
        (1, -1, True, 0),            # minimum to zero
        (1000000, 999999, True, 1999999),  # large amounts
        (1000000, -1000000, True, 0),       # large negative to zero
        (1000000, -1000001, False, 1000000), # large negative exceeding
    ])
    def test_update_bankroll_comprehensive(self, initial_bankroll, change, expected_result, expected_final, class_setup, method_setup):
        """Test bankroll updates with comprehensive scenarios"""
        player = Player.from_name_bankroll("Test Player", initial_bankroll)

        result = player.update_bankroll(change)

        assert result == expected_result
        assert player.bankroll == expected_final

    # ==================== COMPREHENSIVE STATS UPDATE TESTING ====================

    @pytest.mark.parametrize("result_type,money_change,initial_bankroll,should_succeed,expected_bankroll", [
        (Result.VICTORY, 50, 100, True, 150),     # normal victory
        (Result.VICTORY, 0, 100, False, 100),     # victory with no money (invalid)
        (Result.VICTORY, -50, 100, False, 100),   # victory with loss (invalid)
        (Result.DEFEAT, -50, 100, True, 50),      # normal defeat
        (Result.DEFEAT, 0, 100, False, 100),      # defeat with no change (invalid)
        (Result.DEFEAT, 50, 100, False, 100),     # defeat with gain (invalid)
        (Result.DEFEAT, -100, 100, True, 0),      # defeat taking all money
        (Result.DEFEAT, -101, 100, False, 100),   # defeat exceeding bankroll
        (Result.PUSH, 0, 100, True, 100),         # normal push
        (Result.PUSH, 50, 100, True, 100),        # push with money (shouldn't change bankroll)
        (Result.PUSH, -50, 100, True, 100),       # push with negative (shouldn't change)
    ])
    def test_update_stats_comprehensive(self, result_type, money_change, initial_bankroll, should_succeed, expected_bankroll, class_setup, method_setup):
        """Test stats updates with comprehensive scenarios"""
        player = Player.from_name_bankroll("Test Player", initial_bankroll)

        result = player.update_stats((result_type, money_change))

        assert result == should_succeed
        assert player.bankroll == expected_bankroll


class TestExceptionHandling:
    """Comprehensive exception handling tests"""

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
        self.temp_dir = tempfile.mkdtemp()
        yield
        print(f"Tearing down method: {request.function.__name__}")
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    # ==================== EXCEPTION SCENARIOS ====================

    def test_out_of_money_exception_scenarios(self, class_setup, method_setup):
        """Test OutOfMoneyException in various scenarios"""
        # Test with zero bankroll
        broke_player = Player.from_name_bankroll("Broke Player", 0)

        with pytest.raises(OutOfMoneyException):
            broke_player.ante()

    def test_value_error_on_negative_bankroll(self, class_setup, method_setup):
        """Test ValueError when setting negative bankroll"""
        player = Player.from_name_bankroll("Test Player", 100)

        with pytest.raises(ValueError, match="Bankroll cannot be negative"):
            player.bankroll = -1

        with pytest.raises(ValueError, match="Bankroll cannot be negative"):
            player.bankroll = -100

    def test_key_error_on_missing_stats_fields(self, class_setup, method_setup):
        """Test KeyError when accessing missing stats fields"""
        incomplete_stats = {"name": "Incomplete Player"}
        player = Player(incomplete_stats)

        # Should work for name
        assert player.name == "Incomplete Player"

        # Should raise KeyError for missing bankroll
        with pytest.raises(KeyError):
            _ = player.bankroll

    def test_type_error_on_invalid_operations(self, class_setup, method_setup):
        """Test TypeError from invalid operations"""
        # Create player with string bankroll
        invalid_stats = {
            "name": "Invalid Player",
            "bankroll": "not_a_number",
            "wins": 0,
            "losses": 0,
            "pushes": 0
        }
        player = Player(invalid_stats)

        # Should raise TypeError when trying arithmetic
        with pytest.raises(TypeError):
            player.update_bankroll(100)  # Can't add int to string

    def test_json_decode_error_scenarios(self, class_setup, method_setup):
        """Test JSON decode errors in file operations"""
        # Test completely invalid JSON
        invalid_json_path = Path(self.temp_dir) / "invalid.blackjack"
        with open(invalid_json_path, "w") as f:
            f.write("{ this is not valid json }")

        with pytest.raises(json.JSONDecodeError):
            load_player(invalid_json_path)

        # Test truncated JSON
        truncated_json_path = Path(self.temp_dir) / "truncated.blackjack"
        with open(truncated_json_path, "w") as f:
            f.write('{"name": "Test", "bankroll":')  # Incomplete

        with pytest.raises(json.JSONDecodeError):
            load_player(truncated_json_path)

    def test_file_not_found_error_scenarios(self, class_setup, method_setup):
        """Test FileNotFoundError scenarios"""
        # Non-existent file
        with pytest.raises(FileNotFoundError):
            load_player(Path("nonexistent.blackjack"))

        # Non-existent directory
        with pytest.raises(FileNotFoundError):
            save_player(
                Player.from_name_bankroll("Test", 100),
                Path("/nonexistent/dir/player.blackjack")
            )

    def test_permission_error_simulation(self, class_setup, method_setup, mocker):
        """Test PermissionError scenarios"""
        player = Player.from_name_bankroll("Test Player", 100)
        test_path = Path(self.temp_dir) / "readonly.blackjack"

        # Mock open to raise PermissionError
        mock_open = mocker.mock_open()
        mock_open.side_effect = PermissionError("Access denied")

        with mocker.patch("builtins.open", mock_open):
            with pytest.raises(PermissionError):
                save_player(player, test_path)

    def test_index_error_empty_deck(self, class_setup, method_setup):
        """Test IndexError when deck is empty"""
        player = Player.from_name_bankroll("Test Player", 100)
        player.hand = Mock()
        empty_deck = collections.deque()

        # Should raise IndexError when trying to pop from empty deck
        self.fake_input.return_value = "hit"

        with pytest.raises(IndexError):
            player.take_turn(empty_deck)

    def test_attribute_error_scenarios(self, class_setup, method_setup):
        """Test AttributeError scenarios"""
        # Player with None hand trying operations
        player = Player.from_name_bankroll("Test Player", 100)
        player.hand = None

        # Should raise AttributeError when trying to call methods on None
        deck = collections.deque([Mock()])
        self.fake_input.return_value = "hit"

        with pytest.raises(AttributeError):
            player.take_turn(deck)

    # ==================== RECOVERY FROM EXCEPTIONS ====================

    def test_exception_recovery_scenarios(self, class_setup, method_setup):
        """Test that objects can recover from exceptions"""
        player = Player.from_name_bankroll("Recovery Player", 100)

        # Try invalid bankroll update
        try:
            player.update_bankroll(-200)  # Should fail but not crash
        except:
            pass

        # Player should still be functional
        assert player.bankroll == 100
        assert player.update_bankroll(50)
        assert player.bankroll == 150

    def test_file_corruption_recovery(self, class_setup, method_setup):
        """Test recovery from file corruption"""
        player = Player.from_name_bankroll("Original Player", 100)
        file_path = Path(self.temp_dir) / "corruption_test.blackjack"

        # Save valid player
        save_player(player, file_path)

        # Corrupt the file
        with open(file_path, "w") as f:
            f.write("corrupted data")

        # Loading should fail
        with pytest.raises(json.JSONDecodeError):
            load_player(file_path)

        # But we can still save a new player over it
        new_player = Player.from_name_bankroll("New Player", 200)
        save_player(new_player, file_path)

        # And load it successfully
        recovered_player = load_player(file_path)
        assert recovered_player.name == "New Player"
        assert recovered_player.bankroll == 200

    # ==================== STRESS TEST EXCEPTIONS ====================

    def test_rapid_exception_generation(self, class_setup, method_setup):
        """Test rapid generation of exceptions doesn't break system"""
        player = Player.from_name_bankroll("Stress Player", 100)

        # Generate many exceptions rapidly
        for i in range(100):
            try:
                player.update_bankroll(-1000)  # Should fail every time
            except:
                pass

            try:
                player.bankroll = -1  # Should fail every time
            except:
                pass

        # Player should still be functional
        assert player.bankroll == 100
        assert player.update_bankroll(50)
        assert player.bankroll == 150

    def test_nested_exception_scenarios(self, class_setup, method_setup, mocker):
        """Test nested exception scenarios"""
        player = Player.from_name_bankroll("Nested Exception Player", 100)

        # Mock methods to raise exceptions
        original_update = player.update_bankroll

        def failing_update(amount):
            if amount < 0:
                raise ValueError("Simulated failure")
            return original_update(amount)

        player.update_bankroll = failing_update

        # Try operation that would normally work but now fails
        with pytest.raises(ValueError, match="Simulated failure"):
            player.update_stats((Result.DEFEAT, -50))

        # Player state should be preserved
        assert player.bankroll == 100