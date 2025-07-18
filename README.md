# Blackjack Game

A comprehensive command-line Blackjack implementation in Python, featuring proper game mechanics, player persistence, and extensive test coverage. This project is designed as both a playable game and an educational resource for intermediate Python programming.

## Repository Structure

This repository contains three main branches:

### 🎯 **master** - Complete Implementation
- Full working Blackjack game with all features implemented
- Comprehensive documentation and type hints
- Production-ready code following Python best practices

### 📚 **starter_code** - Educational Branch
- Method stubs and class skeletons for the Rochester Makerspace intermediate programming class
- Detailed docstrings explaining expected functionality
- Perfect starting point for students learning Python OOP

### 🧪 **tests** - Testing Branch  
- Complete test suite with 200+ test cases
- Method stubs for implementation practice
- Focuses on test-driven development approach

## Features

### Core Gameplay
- **Standard Blackjack Rules**: Hit, Stand, and Double Down moves
- **Intelligent Ace Handling**: Aces automatically valued at 11 or 1 to prevent busting when possible
- **Dealer AI**: Follows standard casino rules (hits on 16, stands on 17)
- **Proper Scoring**: Handles blackjack (21 with 2 cards), busts, pushes, and standard wins/losses
- **Card Management**: Face-up/face-down card mechanics with proper reveals

### Player Management
- **Persistent Player Data**: JSON-based save/load system for player statistics
- **Bankroll Management**: Track winnings, losses, and enforce betting limits
- **Statistics Tracking**: Comprehensive tracking of wins, losses, pushes, and bankroll changes
- **Input Validation**: Robust handling of invalid user input with helpful error messages

### Technical Excellence
- **Object-Oriented Design**: Clean separation of concerns with proper abstractions
- **Comprehensive Testing**: Edge cases, error scenarios, and integration tests
- **Type Hints**: Full type annotation throughout the codebase
- **Error Handling**: Custom exceptions (`OutOfMoneyException`) and graceful failure recovery
- **Dependency Injection**: Testable design with mockable components

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup
```bash
# Clone the repository
git clone <repository-url>
cd blackjack-game

# Choose your branch based on your needs:
# For complete game:
git checkout master

# For learning/teaching:
git checkout starter_code

# For test-driven development:
git checkout tests

# Install dependencies
pip install -r requirements.txt

# Run the game (master branch only)
python -m Blackjack.main_menu
```

## How to Play

### Starting the Game
Run the main menu and choose from three options:
1. **Play a new game** - Select an existing player and start a hand
2. **Create a new player** - Set up a new player with starting bankroll  
3. **Check player stats** - View win/loss records and current bankroll

### Gameplay Flow
1. **Ante Up**: Place your bet (must be between 1 and your current bankroll)
2. **Initial Deal**: You and dealer each receive two cards (dealer's first card face down)
3. **Player Decisions**:
   - **Hit**: Take another card (can repeat until stand, bust, or 21)
   - **Stand**: Keep current hand and end your turn
   - **Double Down**: Double your bet and receive exactly one more card (if you have sufficient funds)
4. **Dealer Turn**: Dealer reveals hidden card and hits until reaching 17 or higher
5. **Resolution**: Compare hands and update bankroll and statistics

### Winning Conditions
- **Player Blackjack** (21 with 2 cards) beats dealer 21 with 3+ cards
- **Dealer Bust** (over 21) - Player wins if not busted
- **Higher Total** wins (without busting)
- **Tie** results in a push (no money changes hands)
- **Player Bust** always loses, regardless of dealer hand

## Code Architecture

### Core Classes
- **`Card`**: Represents individual playing cards with suit, value, and face up/down state
- **`Hand`**: Manages collections of cards with intelligent ace valuation
- **`Player`**: Handles user input, betting, and statistics persistence  
- **`Dealer`**: Implements house rules and automated play
- **`Game`**: Orchestrates game flow, evaluation, and turn management

### Key Design Patterns
- **Abstract Base Class**: `GameParticipant` defines common interface for Player and Dealer
- **Dependency Injection**: Classes accept optional dependencies for testing
- **Factory Methods**: `Player.from_name_bankroll()` for convenient object creation
- **Strategy Pattern**: Polymorphic `take_turn()` methods for different participant types

## Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest Tests/Unit_Tests/test_player.py

# Run tests with coverage
pytest --cov=Blackjack
```

### Test Categories
- **Unit Tests**: Individual class and method testing
- **Integration Tests**: Full game flow scenarios
- **Edge Case Tests**: Boundary conditions and error scenarios
- **Parameterized Tests**: Comprehensive input validation testing
- **Mock Testing**: Isolated testing with dependency injection

### Test Coverage
- **200+ test cases** covering normal and edge case scenarios
- **File I/O testing** with temporary directories and error simulation
- **Input validation** with comprehensive invalid input testing
- **Game logic verification** including complex ace handling scenarios

## Educational Use

### For Students (starter_code branch)
- Implement methods following detailed docstring specifications
- Learn object-oriented programming principles
- Practice file I/O, exception handling, and user input validation
- Understand game logic implementation and state management

### For Instructors
- Complete test suite provides immediate feedback on implementation
- Progressive difficulty from simple classes to complex game logic
- Real-world application demonstrating multiple programming concepts
- Extensible design allows for additional features (splitting, insurance, etc.)

## File Structure
```
Blackjack/
├── __init__.py
├── card.py              # Card representation and display
├── dealer.py            # Dealer AI and behavior  
├── game.py              # Game flow and rules engine
├── game_participant.py  # Abstract base class
├── hand.py              # Card collection and scoring
├── main_menu.py         # User interface and navigation
├── move.py              # Move enumeration (Hit/Stand/Double)
├── player.py            # Player logic and persistence
├── result.py            # Game result enumeration
├── suit.py              # Card suit enumeration
└── value.py             # Card value enumeration

tests/
├── conftest.py          # Shared test fixtures
├── test_*.py            # Comprehensive test files
└── test_*_edge_cases.py # Additional edge case testing
```

## Contributing

### Code Style
- Follow PEP 8 conventions
- Use type hints for all function signatures
- Write descriptive docstrings for all public methods
- Maintain comprehensive test coverage for new features

### Development Workflow
1. Create feature branch from appropriate base branch
2. Implement functionality with accompanying tests
3. Ensure all tests pass and maintain coverage
4. Submit pull request with detailed description

### TODO
[ ] Write comprehensive integration test suite

## License

This project is designed for educational purposes. Please respect any licensing terms when using for commercial purposes.

## Acknowledgments

Created for the Rochester Makerspace intermediate programming class, with inspiration from classic casino Blackjack rules and modern software engineering practices.
