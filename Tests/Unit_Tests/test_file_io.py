import pytest
import json
import tempfile
from pathlib import Path

from Blackjack.player import Player, save_player, load_player


class TestFileIO:
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
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    # ==================== IMPROVED APPROACHES USING ONLY pytest-mock ====================

    def test_save_player_permission_error_v1(self, class_setup, method_setup, mocker):
        """Approach 1: Mock open() directly with side_effect"""
        player = Player.from_name_bankroll("Test Player", 100)
        test_path = Path(self.temp_dir) / "permission_test.blackjack"

        # Using mocker instead of mock_open
        mocker.patch("builtins.open", side_effect=PermissionError("Access denied"))

        with pytest.raises(PermissionError, match="Access denied"):
            save_player(player, test_path)

    def test_save_player_permission_error_v2(self, class_setup, method_setup, mocker):
        """Approach 2: Mock open() with return value configuration"""
        player = Player.from_name_bankroll("Test Player", 100)
        test_path = Path(self.temp_dir) / "permission_test.blackjack"

        # Create mock that raises exception when called
        mock_open_func = mocker.Mock(side_effect=PermissionError("Access denied"))
        mocker.patch("builtins.open", mock_open_func)

        with pytest.raises(PermissionError):
            save_player(player, test_path)

        # Verify open was called with expected arguments
        mock_open_func.assert_called_once_with(test_path, "w")

    def test_load_player_file_corruption_v1(self, class_setup, method_setup, mocker):
        """Approach 1: Mock file content directly"""
        test_path = Path(self.temp_dir) / "corrupted.blackjack"

        # Mock the file content that would be read
        mock_file_content = "{ invalid json content }"
        mock_file = mocker.mock_open(read_data=mock_file_content)
        mocker.patch("builtins.open", mock_file)

        with pytest.raises(json.JSONDecodeError):
            load_player(test_path)

    def test_load_player_empty_file_better(self, class_setup, method_setup, mocker):
        """Test empty file using mock instead of real file"""
        test_path = Path(self.temp_dir) / "empty.blackjack"

        # Mock empty file content
        mock_file = mocker.mock_open(read_data="")
        mocker.patch("builtins.open", mock_file)

        with pytest.raises(json.JSONDecodeError):
            load_player(test_path)

        # ==================== SOLUTION 1: Intercept json.dump/json.load directly ====================

    def test_save_load_cycle_json_level(self, class_setup, method_setup, mocker):
        player = Player.from_name_bankroll("Mock Player", 500)
        test_path = Path(self.temp_dir) / "mock_cycle.blackjack"

        # Capture what gets serialized during save
        captured_data = None

        def capture_json_dump(data, file_obj):
            nonlocal captured_data
            captured_data = data

        # Mock json.dump to capture data
        mocker.patch("json.dump", side_effect=capture_json_dump)

        # Mock open for save (we don't care about the file, just that it's called)
        mocker.patch("builtins.open", mocker.mock_open())

        # Execute save
        save_player(player, test_path)

        # Verify we captured data
        assert captured_data is not None
        assert captured_data["name"] == "Mock Player"
        assert captured_data["bankroll"] == 500

        # Now mock json.load to return our captured data
        mocker.patch("json.load", return_value=captured_data)

        # Execute load
        loaded_player = load_player(test_path)

        # Verify the cycle worked
        assert loaded_player.name == player.name
        assert loaded_player.bankroll == player.bankroll

    def test_comparison(self, class_setup, method_setup, mocker):
        """NEW WAY: Using only pytest-mock (cleaner)"""
        # No extra imports needed

        player = Player.from_name_bankroll("Test Player", 100)
        test_path = Path(self.temp_dir) / "new_way.blackjack"

        # More concise and readable
        mocker.patch("builtins.open", side_effect=PermissionError("Access denied"))

        with pytest.raises(PermissionError):
            save_player(player, test_path)

    # ==================== ADVANCED PYTEST-MOCK PATTERNS ====================

    def test_multiple_file_operations_sequence(self, class_setup, method_setup, mocker):
        """Test sequence of file operations with different behaviors"""
        player = Player.from_name_bankroll("Sequential Player", 100)
        test_path = Path(self.temp_dir) / "sequential.blackjack"

        # First call succeeds, second fails
        mocker.patch(
            "builtins.open",
            side_effect=[
                mocker.mock_open(
                    read_data='{"name": "old", "bankroll": 50}'
                ).return_value,
                PermissionError("File locked"),
            ],
        )

        # First operation should work
        loaded_player = load_player(test_path)
        assert loaded_player.name == "old"

        # Second operation should fail
        with pytest.raises(PermissionError):
            save_player(player, test_path)

    def test_conditional_mocking_based_on_arguments(
        self, class_setup, method_setup, mocker
    ):
        """Mock different behaviors based on file path"""

        def mock_open_conditional(*args, **kwargs):
            if "readonly" in str(args[0]):
                raise PermissionError("Read-only file")
            elif "missing" in str(args[0]):
                raise FileNotFoundError("File not found")
            else:
                return mocker.mock_open(
                    read_data='{"name": "test", "bankroll": 100}'
                ).return_value

        mocker.patch("builtins.open", side_effect=mock_open_conditional)

        # Test different paths trigger different behaviors
        with pytest.raises(PermissionError):
            load_player(Path("readonly_file.blackjack"))

        with pytest.raises(FileNotFoundError):
            load_player(Path("missing_file.blackjack"))

        # Normal path works
        player = load_player(Path("normal_file.blackjack"))
        assert player.name == "test"
