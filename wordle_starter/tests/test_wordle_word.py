import pytest

from secret_word import WordleWord

# Shorcuts for formating
corr_pos = WordleWord._CORR_POS
corr_ltr = WordleWord._CORR_LTR
wrng_ltr = WordleWord._WRNG_LTR


def test_wordle_set_word():
    """Simple test to determine if hangman word can be set"""
    ww = WordleWord("Tests")
    assert ww._word == "TESTS"


def test_wordle_set_word_fail():
    """Simple test to determine if hangman word can be set"""
    with pytest.raises(ValueError):
        ww = WordleWord("Testing")
        ww.check("tests")


def test_wordle_set_random_word():
    """Test random assignment of hangman word"""
    ww = WordleWord()
    assert len(ww._word) == 5


def test_wordle_word_show_letters():
    """Verify check letters"""
    ww = WordleWord("pizza")

    # correct word
    assert ww.show_letters("PIZZA") == (
        corr_pos.format("P")
        + corr_pos.format("I")
        + corr_pos.format("Z")
        + corr_pos.format("Z")
        + corr_pos.format("A")
    )

    # incorrect word, some correct pos, some correct letter, some wrong letter
    assert ww.show_letters("Plans") == (
        corr_pos.format("P")
        + wrng_ltr.format("L")
        + corr_ltr.format("A")
        + wrng_ltr.format("N")
        + wrng_ltr.format("S")
    )


def test_wordle_word_check():
    "Verify check"
    word = WordleWord("dover")
    assert word.check("dover") is True
    assert word.check("DOVER") is True
    assert word.check("hellos") is False
