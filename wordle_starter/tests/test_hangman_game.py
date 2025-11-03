import pytest

from word_game import GameState, HangmanGame


@pytest.fixture
def hangman_guess_q():
    """
    Creates a Hangman game with 7 turns, secret word "hangman"
    and one incorrect guess

    Returns:
      Instance of the `Hangman` class
    """

    hmg = HangmanGame("hangman", 7)
    hmg.guess("q")
    return hmg


@pytest.fixture
def one_guess_left_hangman():
    """
    Creates a Hangman game with a word "hangman" and makes four incorrect guesses

    Returns:
      Instance of the `Hangman` class
    """

    hmg = HangmanGame("hangman", 5)
    hmg.guess("a")
    hmg.guess("e")
    hmg.guess("i")
    hmg.guess("o")

    return hmg


def test_game_creation():
    """Check game initialization"""
    hm = HangmanGame("test", 5)
    assert hm.guesses == []
    assert hm.secret_word.word == "TEST"
    assert hm.guesses_left == 5


def test_empty_guess(hangman_guess_q):
    """Checks an empty guess

    Args:
        hangman_guess_q (hangman.Game):
            Game of hangman with word set to `hangman`, 7 guesses, and a single guess of q
    """
    prompt = hangman_guess_q.guess()
    assert hangman_guess_q.game_state == GameState.ACTIVE
    assert hangman_guess_q.guesses == ["Q"]
    assert hangman_guess_q.secret_word.word == "HANGMAN"
    assert hangman_guess_q.guesses_left == 6


def test_empty_string_guess(hangman_guess_q):
    """Checks an empty string guess

    Args:
        hangman_guess_q (hangman.Game):
            Game of hangman with word set to `hangman`, 7 guesses and a single guess of q
    """
    prompt = hangman_guess_q.guess()
    assert hangman_guess_q.game_state == GameState.ACTIVE
    assert hangman_guess_q.guesses == ["Q"]
    assert hangman_guess_q.secret_word.word == "HANGMAN"
    assert hangman_guess_q.guesses_left == 6


def test_all_letters(hangman_guess_q):
    """Checks a successful guess of the word by guessing all the letters

    Args:
        hangman_guess_q (hangman.Game):
            Game of hangman with word set to `hangman` and a single guess of q
    """
    hangman_guess_q.guess("h")
    hangman_guess_q.guess("a")
    hangman_guess_q.guess("n")
    hangman_guess_q.guess("g")
    prompt = hangman_guess_q.guess("m")
    assert hangman_guess_q.game_state == GameState.WON
    assert hangman_guess_q.guesses == ["A", "G", "H", "M", "N", "Q"]
    assert hangman_guess_q.guesses_left == 1
    assert hangman_guess_q.secret_word.word == "HANGMAN"


def test_letter_guess(hangman_guess_q):
    """Checks letter guesses, successful, unsuccessful, and repeated

    Args:
        hangman_guess_q (hangman.Game):
            Game of hangman with word set to `hangman` and a single guess of q
    """
    prompt = hangman_guess_q.guess("h")
    assert hangman_guess_q.game_state == GameState.ACTIVE
    assert hangman_guess_q.guesses == ["H", "Q"]
    assert hangman_guess_q.guesses_left == 5

    prompt = hangman_guess_q.guess("w")
    assert hangman_guess_q.game_state == GameState.ACTIVE
    assert hangman_guess_q.guesses == ["H", "Q", "W"]
    assert hangman_guess_q.guesses_left == 4

    prompt = hangman_guess_q.guess("q")
    assert hangman_guess_q.game_state == GameState.ACTIVE
    assert hangman_guess_q.guesses == ["H", "Q", "W"]
    assert hangman_guess_q.guesses_left == 4


def test_last_letter_guess(one_guess_left_hangman):
    """Check correct letter guess on final guess

    Args:
      one_guess_hangman:
        Hangman game with a word "hangman", 5 max guesses, and four incorrect guesses
    """
    prompt = one_guess_left_hangman.guess("h")
    assert one_guess_left_hangman.game_state == GameState.LOST
    assert one_guess_left_hangman.guesses == ["A", "E", "H", "I", "O"]
    assert one_guess_left_hangman.guesses_left == 0


def test_word_guess_wrong(hangman_guess_q):
    """Checks incorrect word guess

    Args:
        hangman_guess_q (hangman.Game):
            Game of hangman with word set to `hangman`,
            with seven guesses and a single guess of q
    """
    prompt = hangman_guess_q.guess("backpay")
    assert hangman_guess_q.game_state == GameState.ACTIVE
    assert hangman_guess_q.guesses == [" ", "Q"]
    assert hangman_guess_q.guesses_left == 5


def test_last_word_guess_wrong(one_guess_left_hangman):
    """Check guess method on final unsuccessful word guess

    Args:
      one_guess_hangman:
        Hangman game with a word "hangman", 5 guesses,  and four incorrect guesses
    """
    prompt = one_guess_left_hangman.guess("backpay")
    assert one_guess_left_hangman.game_state == GameState.LOST
    assert one_guess_left_hangman.guesses == [" ", "A", "E", "I", "O"]
    assert one_guess_left_hangman.guesses_left == 0


def test_last_word_guess_correct(one_guess_left_hangman):
    """Check guess method on final unsuccessful word guess

    Args:
      one_guess_hangman:
        Hangman game with a word "hangman" and four incorrect guesses
    """
    prompt = one_guess_left_hangman.guess("hangman")
    assert one_guess_left_hangman.game_state == GameState.WON
    assert one_guess_left_hangman.guesses == [" ", "A", "E", "I", "O"]
    assert one_guess_left_hangman.guesses_left == 0


def test_format_prompt_initial():
    """Test _format_prompt with no guesses (initial game state)"""
    hm = HangmanGame("tests", 5)
    prompt = hm._format_prompt()

    assert "Welcome to Hangman" in prompt
    assert "Number of guesses remaining: 5" in prompt
    assert "Please Enter a Letter or Guess the word" in prompt
    assert "_ _ _ _ _" in prompt


def test_format_prompt_none_guess(hangman_guess_q):
    """Test _format_prompt with None as guess after game has started

    Args:
        hangman_guess_q (HangmanGame):
            Game with word set to `hangman`, 7 guesses, and single guess of q
    """
    prompt = hangman_guess_q._format_prompt(None)

    assert "Number of guesses remaining: 6" in prompt
    assert "Please Enter a Letter or Guess the word" in prompt
    assert "Guesses: Q" in prompt


def test_format_prompt_empty_string(hangman_guess_q):
    """Test _format_prompt with empty string as guess

    Args:
        hangman_guess_q (HangmanGame):
            Game with word set to `hangman`, 7 guesses, and single guess of q
    """
    prompt = hangman_guess_q._format_prompt("")

    assert "Number of guesses remaining: 6" in prompt
    assert "Please Enter a Letter or Guess the word" in prompt


def test_format_prompt_letter_guess_active(hangman_guess_q):
    """Test _format_prompt with letter guess and game still active

    Args:
        hangman_guess_q (HangmanGame):
            Game with word set to `hangman`, 7 guesses, and single guess of q
    """
    hangman_guess_q._guesses.append("H")
    prompt = hangman_guess_q._format_prompt()

    assert "Number of guesses remaining: 5" in prompt
    assert "Please Enter a Letter or Guess the word" in prompt
    assert "H" in prompt
    assert "_" in prompt


def test_format_prompt_all_letters_guessed(hangman_guess_q):
    """Test _format_prompt when all letters are guessed correctly

    Args:
        hangman_guess_q (HangmanGame):
            Game with word set to `hangman`, 7 guesses, and single guess of q
    """
    hangman_guess_q._guesses = ["H", "A", "N", "G", "M", "Q"]
    hangman_guess_q._game_state = GameState.WON
    prompt = hangman_guess_q._format_prompt()

    assert "You guessed" in prompt
    assert "H A N G M A N" in prompt
    assert "Number of guesses remaining" not in prompt


def test_format_prompt_correct_word_guess(hangman_guess_q):
    """Test _format_prompt when word is guessed correctly

    Args:
        hangman_guess_q (HangmanGame):
            Game with word set to `hangman`, 7 guesses, and single guess of q
    """
    hangman_guess_q._game_state = GameState.WON
    prompt = hangman_guess_q._format_prompt("hangman")

    assert "You guessed the word" in prompt
    assert "Word:" in prompt
    assert "H A N G M A N" in prompt


def test_format_prompt_incorrect_word_guess(hangman_guess_q):
    """Test _format_prompt with incorrect word guess and guesses remaining

    Args:
        hangman_guess_q (HangmanGame):
            Game with word set to `hangman`, 7 guesses, and single guess of q
    """
    prompt = hangman_guess_q._format_prompt("testing")

    assert "Incorrect guess" in prompt
    assert "Number of guesses remaining: 6" in prompt
    assert "Please Enter a Letter or Guess the word" in prompt


def test_format_prompt_game_lost_letter(one_guess_left_hangman):
    """Test _format_prompt when game is lost (no guesses left) with letter guess

    Args:
        one_guess_left_hangman (HangmanGame):
            Game with word "hangman", 5 guesses, and four incorrect guesses
    """
    one_guess_left_hangman._guesses.append("Z")
    one_guess_left_hangman._game_state = GameState.LOST
    prompt = one_guess_left_hangman._format_prompt()

    assert "You are out of turns: game over" in prompt
    assert "Word:" in prompt
    assert "H A N G M A N" in prompt
    assert "Please Enter a Letter or Guess the word" not in prompt


def test_format_prompt_game_lost_word(one_guess_left_hangman):
    """Test _format_prompt when game is lost with incorrect word guess

    Args:
        one_guess_left_hangman (HangmanGame):
            Game with word "hangman", 5 guesses, and four incorrect guesses
    """
    one_guess_left_hangman._game_state = GameState.LOST
    prompt = one_guess_left_hangman._format_prompt("testing")

    assert "Incorrect guess" in prompt
    assert "You are out of turns: game over" in prompt
    assert "Word:" in prompt
    assert "Please Enter a Letter or Guess the word" not in prompt
