import pytest

from game_runner import GameRunner, GameType


def create_mock_input(responses):
    """
    Generates a mock input function that returns responses from the supplied list

    Arguments:
        responses:
            a list of values that will be used as mock input

    Return:
        function named `get_input` that generates a mock input responses based
        each time it is called to simulate user input during testing.
    """

    # Create a generator for responses
    # https://docs.python.org/3/tutorial/classes.html#generators
    generator = (response for response in responses)

    def get_input(prompt):
        return next(generator)

    return get_input


def test_pass_all_wordle(monkeypatch):
    """Check `process_args()` when both turns and word are submitted.
    Use `monkeypatch` to override`sys.argv`

    Arguments:
        monkeypatch:
            Monkeypatch is a pytest fixture that allows you to modify the behavior of
            objects, functions, or classes during testing. It is used to replace sys.argv
            for this test.
    """
    monkeypatch.setattr("sys.argv", ["game_runner", "wordle", "tests"])
    runner = GameRunner()
    assert runner.game_type == GameType.WORDLE
    assert runner.turns == 5
    assert runner.word == "tests"


def test_wordle(monkeypatch):
    """Check `process_args()` when only turns but not word is submitted.
    Use `monkeypatch` to override`sys.argv`

    Arguments:
        monkeypatch:
            Monkeypatch is a pytest fixture that allows you to modify the behavior of
            objects, functions, or classes during testing. It is used to replace sys.argv
            for this test.
    """
    monkeypatch.setattr(
        "sys.argv",
        ["game_runner", "wordle"],
    )
    runner = GameRunner()
    assert runner.game_type == GameType.WORDLE
    assert runner.turns == 5
    assert runner.word is None


def test_wordle_correct_guess(monkeypatch, capsys):
    """
    Test Wordle game where the player guesses the word correctly.

    Arguments:
        monkeypatch:
            Pytest fixture to modify behavior during testing.

        capsys:
            Pytest fixture to capture stdout/stderr.
    """
    mock_input = create_mock_input(["tests", ""])
    monkeypatch.setattr("builtins.input", mock_input)
    monkeypatch.setattr("sys.argv", ["game_runner", "wordle", "tests"])

    runner = GameRunner()
    runner.run()
    captured = capsys.readouterr()

    assert "Welcome to Wordle" in captured.out
    assert "You guessed the word" in captured.out


def test_wordle_multiple_guesses(monkeypatch, capsys):
    """
    Test Wordle game with multiple incorrect guesses before correct one.

    Arguments:
        monkeypatch:
            Pytest fixture to modify behavior during testing.

        capsys:
            Pytest fixture to capture stdout/stderr.
    """
    mock_input = create_mock_input(["wrong", "guess", "tests", ""])
    monkeypatch.setattr("builtins.input", mock_input)
    monkeypatch.setattr("sys.argv", ["game_runner", "wordle", "tests"])

    runner = GameRunner()
    runner.run()
    captured = capsys.readouterr()

    assert "Welcome to Wordle" in captured.out
    assert "Number of guesses remaining: 5" in captured.out
    assert "Number of guesses remaining: 4" in captured.out
    assert "Number of guesses remaining: 3" in captured.out
    assert "You guessed the word" in captured.out


def test_wordle_lose_game(monkeypatch, capsys):
    """
    Test Wordle game where player runs out of guesses and loses.

    Arguments:
        monkeypatch:
            Pytest fixture to modify behavior during testing.

        capsys:
            Pytest fixture to capture stdout/stderr.
    """
    mock_input = create_mock_input(["wrong", "guess", "again", "nopes", "fails", ""])
    monkeypatch.setattr("builtins.input", mock_input)
    monkeypatch.setattr("sys.argv", ["game_runner", "wordle", "tests"])

    runner = GameRunner()
    runner.run()
    captured = capsys.readouterr()

    assert "Welcome to Wordle" in captured.out
    assert "You are out of turns: game over" in captured.out
    assert "Word: TESTS" in captured.out


def test_wordle_invalid_length_guess(monkeypatch, capsys):
    """
    Test Wordle game handling invalid length guesses (not 5 letters).

    Arguments:
        monkeypatch:
            Pytest fixture to modify behavior during testing.

        capsys:
            Pytest fixture to capture stdout/stderr.
    """
    mock_input = create_mock_input(["test", "", "tests", ""])
    monkeypatch.setattr("builtins.input", mock_input)
    monkeypatch.setattr("sys.argv", ["game_runner", "wordle", "tests"])

    runner = GameRunner()
    runner.run()
    captured = capsys.readouterr()

    assert "Welcome to Wordle" in captured.out
    # Invalid guess shouldn't count, so still have 5 guesses after "test"
    assert captured.out.count("Number of guesses remaining: 5") >= 2
    assert "You guessed the word" in captured.out
