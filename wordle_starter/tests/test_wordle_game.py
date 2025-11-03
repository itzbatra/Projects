import pytest

from word_game import GameState, WordleGame


@pytest.fixture
def wordle_one_guess():
    """
    Creates a Wordle game with 5 turns, secret word "hangs" and one incorrect guess
    "laugh"

    Returns:
      WordleGame
    """

    wg = WordleGame("hangs")
    wg.guess("laugh")
    return wg


@pytest.fixture
def one_guess_left_wordle():
    """
    Creates a Wordle game with a word "hangs" and with four
    incorrect guesses:
        laugh
        saint
        haunt
        handy

    Returns:
      WordleGame
    """

    wg = WordleGame("hangs")
    wg.guess("laugh")
    wg.guess("saint")
    wg.guess("haunt")
    wg.guess("handy")

    return wg


def test_init():
    """Check initial game setup"""
    wg = WordleGame("tests")
    assert wg.game_state == GameState.ACTIVE
    assert wg.guesses_left == 5
    assert wg.guesses == []
    assert wg.secret_word.word == "TESTS"


def test_init_empty():
    """Check initial game setup"""
    wg = WordleGame()
    assert wg.game_state == GameState.ACTIVE
    assert wg.guesses_left == 5
    assert wg.guesses == []
    assert len(wg.secret_word.word) == 5


def test_empty_guess(wordle_one_guess):
    """Checks an empty guess

    Args:
        hangman_guess_q (hangman.Game):
            Game of wordle with word set to `hangs` and a single guess of 'laugh'
    """
    prompt = wordle_one_guess.guess()
    assert wordle_one_guess.game_state == GameState.ACTIVE
    assert wordle_one_guess.guesses == ["LAUGH"]
    assert wordle_one_guess.guesses_left == 4


def test_empty_string_guess(wordle_one_guess):
    """Checks an empty string guess

    Args:
        wordle_one_guess(WordleGame):
            Game with word set to `hangs` and a single guess of "laugh"
    """
    prompt = wordle_one_guess.guess("")
    assert wordle_one_guess.game_state == GameState.ACTIVE
    assert wordle_one_guess.guesses_left == 4
    assert wordle_one_guess.guesses == ["LAUGH"]


def test_word_guess_wrong(wordle_one_guess):
    """Checks incorrect word guess

    Args:
        one_guess_left_wordle (WordleGame)
            Game of wordle with word set to `hangs` and a single guess of 'laugh'
    """
    prompt = wordle_one_guess.guess("backs")
    assert wordle_one_guess.game_state == GameState.ACTIVE
    assert wordle_one_guess.guesses_left == 3
    assert wordle_one_guess.guesses == ["LAUGH", "BACKS"]


def test_last_word_guess_wrong(one_guess_left_wordle):
    """Check guess method on final unsuccessful word guess

    Args:
      one_guess_left_wordle:
        Hangman game with a word "hangman" and four incorrect guesses
            laugh
            saint
            haunt
            handy

    """
    prompt = one_guess_left_wordle.guess("backs")
    assert one_guess_left_wordle.game_state == GameState.LOST
    assert one_guess_left_wordle.guesses_left == 0
    assert one_guess_left_wordle.guesses == [
        "LAUGH",
        "SAINT",
        "HAUNT",
        "HANDY",
        "BACKS",
    ]


def test_last_word_guess_correct(one_guess_left_wordle):
    """Check guess method on final successful word guess

    Args:
      one_guess_left_wordle:
        Hangman game with a word "hangs" and four incorrect guesses
            laugh
            saint
            haunt
            handy

    """
    prompt = one_guess_left_wordle.guess("hangs")
    assert one_guess_left_wordle.game_state == GameState.WON
    assert one_guess_left_wordle.guesses_left == 0
    assert one_guess_left_wordle.guesses == [
        "LAUGH",
        "SAINT",
        "HAUNT",
        "HANDY",
        "HANGS",
    ]


def test_format_prompt_initial(wordle_one_guess):
    """Test _format_prompt with no guesses (initial game state)

    Args:
        wordle_one_guess (WordleGame):
            Game with word set to `hangs` and a single guess of "laugh"
    """
    wg = WordleGame("tests")
    prompt = wg._format_prompt()

    assert "Welcome to Wordle" in prompt
    assert "Number of guesses remaining: 5" in prompt
    assert "Enter a five letter word guess:" in prompt


def test_format_prompt_none_guess(wordle_one_guess):
    """Test _format_prompt with None as guess after game has started

    Args:
        wordle_one_guess (WordleGame):
            Game with word set to `hangs` and a single guess of "laugh"
    """
    prompt = wordle_one_guess._format_prompt(None)

    assert "Number of guesses remaining: 4" in prompt
    assert "Enter a five letter word guess:" in prompt


def test_format_prompt_empty_string(wordle_one_guess):
    """Test _format_prompt with empty string as guess

    Args:
        wordle_one_guess (WordleGame):
            Game with word set to `hangs` and a single guess of "laugh"
    """
    prompt = wordle_one_guess._format_prompt("")

    assert "Number of guesses remaining: 4" in prompt
    assert "Enter a five letter word guess:" in prompt


def test_format_prompt_invalid_length(wordle_one_guess):
    """Test _format_prompt with word of incorrect length

    Args:
        wordle_one_guess (WordleGame):
            Game with word set to `hangs` and a single guess of "laugh"
    """
    prompt = wordle_one_guess._format_prompt("test")

    assert "Number of guesses remaining: 4" in prompt
    assert "Enter a five letter word guess:" in prompt


def test_format_prompt_correct_guess(wordle_one_guess):
    """Test _format_prompt when word is guessed correctly

    Args:
        wordle_one_guess (WordleGame):
            Game with word set to `hangs` and a single guess of "laugh"
    """
    wordle_one_guess._game_state = GameState.WON
    prompt = wordle_one_guess._format_prompt("hangs")

    assert "You guessed the word" in prompt
    assert "Number of guesses remaining" not in prompt


def test_format_prompt_incorrect_with_guesses_left(wordle_one_guess):
    """Test _format_prompt with incorrect guess and guesses remaining

    Args:
        wordle_one_guess (WordleGame):
            Game with word set to `hangs` and a single guess of "laugh"
    """
    prompt = wordle_one_guess._format_prompt("tests")

    assert "Number of guesses remaining: 4" in prompt
    assert "Enter a five letter word guess:" in prompt


def test_format_prompt_game_lost(one_guess_left_wordle):
    """Test _format_prompt when game is lost (no guesses left)

    Args:
        one_guess_left_wordle (WordleGame):
            Game with word "hangs" and four incorrect guesses
    """
    one_guess_left_wordle._guesses.append("tests")
    one_guess_left_wordle._game_state = GameState.LOST
    prompt = one_guess_left_wordle._format_prompt("tests")
    assert "You are out of turns: game over" in prompt
    assert "Word:" in prompt
    assert "Enter a five letter word guess:" not in prompt
