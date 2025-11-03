import pathlib
import random


class HangmanWord:
    """Represents a secret word for the game hangman. Players can guess letters
    to reveal the word used and check if their guess is the secret word

    Class Attributes:
        WORD_FILE_PATH (pathlib.Path):
            Path to word file for selection of random word when initializing
            HangmanWord

    Attributes:
        _word (str):
            Uppercase stored word
    """

    WORD_FILE_PATH: pathlib.Path = pathlib.Path(__file__).parent.resolve() / "words.txt"

    def __init__(self, word: str | None = None):
        """Initialize secret word with the word parameter or select random word if
        none are specified.

        Args:
          word (str | None):
            the word to be guessed optional.

        Attributes:
            _word (str): uppercase word to be guessed
        """
        if word is None:
            self._word: str = self.random_word()
        else:
            self._word = word.upper()

    @property
    def word(self):
        """Defines a property to access "_word" since it shouldn't be set
        directly

        Returns:
            str:
                raw _word
        """
        return self._word

    def check(self, word: str) -> bool:
        """Compares a the given word with the _word attribute after converting
        to uppercase and return true if they are the same, false if they differ.

        Args:
          word (str):
            word to compare to the `_word` attribute

        Returns:
            bool:
                indicates if the input `word` is equal to the `_word` attribute
        """
        return word.upper() == self._word

    @property
    def formatted_word(self) -> str:
        """
        Adds a space after each letter in _word and and then removes the extra space at
        the end before returning the modified word.

        Return:
            str:
                where each letter of the word stored in the `_word` attribute is
                separated by a space
        """
        out_string = ""

        for letter in self._word:
            out_string += letter + " "

        # Remove the last space extraneous space to match the test cases
        return out_string.strip()

    def show_letters(self, guess: str | list[str]) -> str:
        """Takes a list of guessed letters and returns a string showing the
        letters guessed correctly in the word and underscores for letters
        not yet guessed.

        Args:
            guessed_letter (str | list[str]):
                a list of guessed letters

        Returns:
            str:
                the letters of the word being guessed, with underscores for
                letters that have not been guessed yet.
        """

        out_string = ""

        # Capitalize all of the guesses so they match the case of letters in the _word
        guesses = "".join(guess).upper()

        # Construct out_string with each letter in the guesses or a underscore
        # for each of the unguessed letters in the secret word
        for letter in self._word:
            if letter in guesses:
                out_string += letter
            else:
                out_string += "_"
            out_string += " "

        # Remove the last space extraneous space to match the test cases
        return out_string.strip()

    def check_letters(self, guess: list[str]) -> bool:
        """Compares the unique uppercase letters in a guess with the unique
        letters in a word returning true if all the letters match.

        Args:
          guess (list[str]):
            list of letters to be compared with the letters in the`_word`
            attribute of the object.

        Returns:
            bool:
                True if the set letters in the guess matches the set of letters
                in the _word otherwise False.
        """
        # Capitalize all guess_letters so they will match the letters in _word
        guess_letters = set("".join(guess).upper())

        if set(self._word).issubset(guess_letters):
            return True
        else:
            return False

    @classmethod
    def random_word(cls):
        """
        Reads a file containing words, selects a random word
        from the file, removes trailing spaces, and returns it in upper case.

        Args:
          obj:
            a reference to the class itself.  Here it is used to access the class
            variable `WORD_FILE_PATH` to read a random word

        Returns:
           str randomly chosen word from a file specified by the `WORD_FILE_PATH`
           attribute converted to upper case
        """
        with open(cls.WORD_FILE_PATH) as words_file:
            words = words_file.readlines()
            if len(words) == 0:
                raise ValueError(f"The {cls.WORD_FILE_PATH} file is empty")
            else:
                word = random.choice(words).strip().upper()
        return word
