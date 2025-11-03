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


def test_pass_all_hangman(monkeypatch):
    """Check `process_args()` when both turns and word are submitted.
    Use `monkeypatch` to override`sys.argv`

    Arguments:
        monkeypatch:
            Monkeypatch is a pytest fixture that allows you to modify the behavior of
            objects, functions, or classes during testing. It is used to replace sys.argv
            for this test.
    """
    monkeypatch.setattr("sys.argv", ["game_runner", "hangman", "5", "testing"])
    runner = GameRunner()
    assert runner.game_type == GameType.HANGMAN
    assert runner.turns == 5
    assert runner.word == "testing"


def test_pass_turns_hangman(monkeypatch):
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
        [
            "game_runner",
            "hangman",
            "9",
        ],
    )
    runner = GameRunner()
    assert runner.game_type == GameType.HANGMAN
    assert runner.turns == 9
    assert runner.word is None


def test_pass_none(monkeypatch):
    """Check `process_args()` when neither turns or word are submitted.
    Use `monkeypatch` to override`sys.argv`

    Arguments:
        monkeypatch:
            Monkeypatch is a pytest fixture that allows you to modify the behavior of
            objects, functions, or classes during testing. It is used to replace sys.argv
            for this test.
    """
    monkeypatch.setattr("sys.argv", ["game_runner"])
    with pytest.raises(SystemExit):
        runner = GameRunner()


def test_hangman_letter_guesses(monkeypatch, capsys):
    """
    Test Hangman game where the player successfully guesses letters
    to reveal a hidden word.

    Arguments:
        monkeypatch:
            The `monkeypatch` fixture in pytest is used to modify the behavior of
            objects, functions, or variables during testing. It allows you to
            replace attributes, functions, or classes. In this case it will be
            used to override sys.argv and input.

        capsys:
            The `capsys` fixture in pytest is used to capture the standard output
            and standard error streams during the execution of a test function.
    """
    mock_input = create_mock_input(["t", "e", "s", ""])
    monkeypatch.setattr("builtins.input", mock_input)
    monkeypatch.setattr("sys.argv", ["game_runner", "hangman", "3", "test"])

    runner = GameRunner()
    runner.run()
    captured = capsys.readouterr()

    assert "Welcome to Hangman" in captured.out
    assert "T _ _ T" in captured.out
    assert "T E _ T" in captured.out
    assert "You guessed" in captured.out
    assert "T E S T" in captured.out


def test_hangman_word_guess(monkeypatch, capsys):
    """
    Test Hangman game where the player successfully guesses the word directly.

    Arguments:
        monkeypatch:
            Pytest fixture to modify behavior during testing.

        capsys:
            Pytest fixture to capture stdout/stderr.
    """
    mock_input = create_mock_input(["hand", ""])
    monkeypatch.setattr("builtins.input", mock_input)
    monkeypatch.setattr("sys.argv", ["game_runner", "hangman", "3", "hand"])

    runner = GameRunner()
    runner.run()
    captured = capsys.readouterr()

    assert "Welcome to Hangman" in captured.out
    assert "You guessed the word" in captured.out
    assert "H A N D" in captured.out


def test_hangman_lose_game(monkeypatch, capsys):
    """
    Test Hangman game where the player runs out of guesses and loses.

    Arguments:
        monkeypatch:
            Pytest fixture to modify behavior during testing.

        capsys:
            Pytest fixture to capture stdout/stderr.
    """
    mock_input = create_mock_input(["q", "z", ""])
    monkeypatch.setattr("builtins.input", mock_input)
    monkeypatch.setattr("sys.argv", ["game_runner", "hangman", "2", "test"])

    runner = GameRunner()
    runner.run()
    captured = capsys.readouterr()

    assert "Welcome to Hangman" in captured.out
    assert "You are out of turns: game over" in captured.out
    assert "Word: T E S T" in captured.out
