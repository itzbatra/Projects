from secret_word import HangmanWord


def test_hangman_set_word():
    """Simple test to determine if hangman word can be set"""
    sw = HangmanWord("Testing")
    assert sw._word == "TESTING"


def test_hangman_set_random_word():
    """Test random assignment of hangman word"""
    sw = HangmanWord()
    with open(HangmanWord.WORD_FILE_PATH) as words_file:
        words = words_file.readlines()
        words = "".join(words).upper()
    assert sw._word in words


def test_hangman_word_show_letters():
    "Verify letter output of hangman show letters"
    word = HangmanWord("vancouver")
    assert word.show_letters(["V"]) == "V _ _ _ _ _ V _ _"
    assert word.show_letters(["V", "A"]) == "V A _ _ _ _ V _ _"


def test_hangman_word_check_letters():
    """Verify check letters"""
    word = HangmanWord("pizza")
    # Check Valid Letters
    assert word.check_letters(["P", "I", "Z", "A"]) is True

    # Check out of order different cases
    assert word.check_letters(["a", "Z", "p", "I"]) is True

    # Check differnt letters
    assert word.check_letters(["R", "I", "S", "E"]) is False

    # Check with extra letters
    assert word.check_letters(["Q", "P", "I", "Z", "A"]) is True

    # Check wrong letter
    word = HangmanWord("Tim")
    assert word.check_letters(["G"]) is False


def test_hangman_word_check():
    "Verify check"
    word = HangmanWord("vancouver")
    assert word.check("VanCOuver") is True
    assert word.check("VANCOUVER") is True
    assert word.check("hello") is False
