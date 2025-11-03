import abc
import pathlib
import random

# Colorama is used to format the terminal output it must be initialized
import colorama


class SecretWord(abc.ABC):
    """Represents a secret word for the game hangman. Players can guess letters
    to reveal the word used and check if their guess is the secret word

    Class Attributes:
        WORD_FILE_PATH (pathlib.Path):
            Path to word file for selection of random word when initializing
            SecretWord

    Attributes:
        _word (str):
            Uppercase stored word
    """

    WORD_FILE_PATH: pathlib.Path = pathlib.Path(__file__).parent.resolve() / "words.txt"

    def __init__(self, word=None):
        """Initialize secret word with the word parameter or select random word if
        none are specified.

        Args:
          word (str):
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
    @abc.abstractmethod
    def formatted_word(self) -> str:
        """Return subclass specific form of formatted SecretWord value

        Return:
            str:
                subclass specific version of formatted SecretWord value
        """
        pass

    @abc.abstractmethod
    def show_letters(self, guess: str | list[str]) -> str:
        """Create string showing the result of a guess.  Indicating what letters
        matched and which letters did not match any in the secret word

        Args:
            guess (str | list[str]):
                a list of letters or string

        Returns:
            str:
                string representation of guess result
        """
        pass

    @classmethod
    @abc.abstractmethod
    def random_word(cls) -> str:
        """Reads a file containing words, selects a random word
        from the file according subclass requirements

        Returns:
            str:
                randomly chosen word from a file specified by the
                `WORD_FILE_PATH`
        """
        pass


class WordleWord(SecretWord):
    """A secret word for the game Wordle.

    Class Attributes:

        WORD_LENGTH (int):
            length of all Wordle words

        _EMPTY_WORD (str):
            an all spaces Wordle word

        _CORR_POS (str):
            template for formatting when the letter is a Correct Letter,
            in the Correct position

        _CORR_LTR (str):
            template for formatting when its the letter is a Correct Letter,
            but in the wrong position, i.e. the letter is in secret word at
            a different position

        _WRNG_LTR (str):
            template for formatting a leter when it the letter is
            is an Incorrect Letter, i.e. the letter is not in the secret word

    Attributes:

        _word (str):
            uppercase word

    """

    WORD_LENGTH = 5  # All words to be guessed are 5 letters long
    _EMPTY_WORD = f"{WORD_LENGTH * ' '}"  # five spaces one for each letter

    # Formats for outputting letters
    _CORR_POS = (
        f"{colorama.Back.GREEN}{colorama.Fore.WHITE}"
        + f"{colorama.Style.BRIGHT}{{0}}{colorama.Style.RESET_ALL}"
    )

    _CORR_LTR = (
        f"{colorama.Back.YELLOW}{colorama.Fore.WHITE}{{0}}{colorama.Style.RESET_ALL}"
    )

    _WRNG_LTR = (
        f"{colorama.Back.LIGHTBLACK_EX}{colorama.Fore.WHITE}"
        + f"{{0}}{colorama.Style.RESET_ALL}"
    )

    # Incorrect Letter: letter is not in secret word
    def __init__(self, word=None):
        """Initialize secret word with the word parameter or select random word if
        none are specified.

        Args:
          word:
            the word to be guessed optional.
        """
        # word must be empty or a 5 letter word
        if (word is None) or (isinstance(word, str) and len(word) == self.WORD_LENGTH):
            super().__init__(word)
        else:
            raise ValueError("Wordle word must be 5 letters long or randomly selected")

        # Initialize colorama to allow coloured display
        colorama.init()

    @property
    def formatted_word(self) -> str:
        """Formats internal word to returning a form where every letter is
        formatted using the _COR_POS formatting

        Return:
            str
                the letters of the word stored in the `_word` attribute, each
                wrapped with _CORR_POS formatting
        """
        out_string = ""

        for letter in self._word:
            out_string += self._CORR_POS.format(letter)

        return out_string

    def show_letters(self, guess: str | list[str]):
        """Formats guess to show where letters are in the correct position,
        in the wrong position but in the _word, or not in the _word.


        Args:
          guess (str | list[str]):
            a word or list of guessed letters, the list is allowed to work
            with superclass SecretWord

        Returns:
            str:
                with the letters of the word being guessed, with per letter
                formatting.
        """

        out_string = ""

        # if the guess is passed as a list of letters combine them into a single word
        if isinstance(guess, list):
            guess = "".join(guess)

        # Capitalize all of the guess so they match the case of letters in the _word
        guess = guess.upper()

        # verify valid the guess is a valid wordle word
        if len(guess) != 0 and len(guess) != self.WORD_LENGTH:
            raise AttributeError("Wordle word guess must be 5 characters long")

        elif len(guess) == 0:  # But Allow empty guess for initial display of letters
            guess = self._EMPTY_WORD

        for pos in range(0, self.WORD_LENGTH):
            if guess[pos] == self._word[pos]:
                out_string += self._CORR_POS.format(guess[pos])
            elif guess[pos] in self._word:
                out_string += self._CORR_LTR.format(guess[pos])
            else:
                out_string += self._WRNG_LTR.format(guess[pos])

        return out_string

    @classmethod
    def random_word(cls):
        """Reads a file containing words, selects a random five letter word
        from the file, removes trailing spaces, and returns it in upper case.

        Args:
            obj:
                a reference to the class itself.  Here it is used to access the class
                variable `WORD_FILE_PATH` to read a random word

        Returns:
            str:
                randomly chosen word from a file specified by the `WORD_FILE_PATH`
                attribute converted to upper case
        """
        with open(cls.WORD_FILE_PATH) as words_file:
            five_letter_words = []
            for word in words_file:
                clean_word = word.strip()
                if len(clean_word) == cls.WORD_LENGTH:
                    five_letter_words.append(clean_word.upper())

        return random.choice(five_letter_words)

# class HangmanWord(SecretWord):
#     """Represents a secret word for the game hangman. Players can guess letters
#     to reveal the word used and check if their guess is the secret word
#     """
#     pass
class HangmanWord(SecretWord):
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
        super().__init__(word)

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
