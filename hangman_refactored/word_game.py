import enum
import json
import pathlib
import sys

from secret_word import HangmanWord


class GameState(enum.Enum):
    """Enumeration with three states: ACTIVE, WON, and LOST."""

    ACTIVE = 1
    WON = 2
    LOST = 3


class HangmanGame:
    """The Hangman class encapsulates the logic of a hangman game.  It allows
    the setting of a secret word and allows players guess letters or the secret word.
    Only allowing the specified number of attempts.

    Class Attributes:
        _GUESS_PROMPT (str):
            prompt for user guess
        _GUESSES_REMIANING (str):
            prompt to tell user the remaining guesses
        _CORRECT_GUESS (str):
            prompt to tell user they guessed correctly
        _INCORRECT_GUESS (str):
            prompt to tell user they guessed incorrectly
        _OUT_OF_TURNS (str):
            prompt to inform user that they are out of turns
        _CLR_SCRN (str):
            terminal code that clears the screen
        RESTORE_FILE_PATH (pathlib.Path):
            file path for saving and restoring game state
        _GAME_START (str):
            greeting for new game prompt

    Attributes:
        _game_state (GameState): if the game is in progress, won, or lost
        _max_turns (int): maximum number of guesses or turns in the game
        _guesses (list[str]): user guesses of secret word
        _secret_word (HangmanWord):
            HangmanWord object used to manage secret word.
    """

    # Strings for player prompts
    _GUESS_PROMPT = "Please Enter a Letter or Guess the word"
    _GUESSES_REMAINING = "Number of guesses remaining:"
    _CORRECT_GUESS = "You guessed the word\n"
    _INCORRECT_GUESS = "Incorrect guess\n"
    _OUT_OF_TURNS = "You are out of turns: game over\n"
    _CLR_SCRN = "\033[H\033[J"
    _GAME_START = "\nWelcome to Hangman\n"

    RESTORE_FILE_PATH: pathlib.Path = (
        pathlib.Path(__file__).parent.resolve() / "game_save.json"
    )

    def __init__(self, word: str | None = None, turns: int | None = None):
        """
        Initializes the game with a specified number of turns, secret word, and an
        empty list for guesses. If no word is supplied a random word is selected.

        Args:
          self:
            reference the current game object.
          turns:
            number of attempts to guess the word
          word:
            data to store in the _secret_word attribute
        """
        if turns is None or not isinstance(turns, int):
            turns = 10

        self._game_state = GameState.ACTIVE
        self._max_turns = turns
        self._guesses = []
        self.secret_word = word

    @property
    def game_state(self) -> GameState:
        return self._game_state

    @property
    def guesses(self) -> list[str]:
        return sorted(self._guesses)

    @property
    def secret_word(self) -> HangmanWord:
        return self._secret_word

    @secret_word.setter
    def secret_word(self, word):
        self._secret_word = HangmanWord(word)

    @property
    def guesses_left(self):
        """
        Calculates the number of turns left based on the maximum turns allowed and the
        turns already taken.

        Returns:

        the number of turns remaining
        """

        return self._max_turns - len(self._guesses)

    def _format_prompt(self, guess=None) -> str:
        """Create prompt for user for next step in game"""

        # Add clear screen to every prompt
        prompt = self._CLR_SCRN + "\n"

        # No guesses intial prompt
        if len(self._guesses) == 0:
            prompt += (
                self._GAME_START
                + self._secret_word.show_letters(self._guesses)
                + "\n"
                + f"{self._GUESSES_REMAINING} {self.guesses_left}\n\n"
                + self._GUESS_PROMPT
            )

        elif self._game_state == GameState.WON:
            if isinstance(guess, str):
                # Successful word guess: user won
                prompt += (
                    f"Word: {self._secret_word.formatted_word}\n"
                    + f"{self._CORRECT_GUESS}\n"
                )
            else:  # successfull letter guess
                prompt += (
                    f"{self._secret_word.show_letters(self._guesses)}\n"
                    + f"Guesses: {''.join(sorted(self._guesses)).strip()}\n"
                    + f"{self._CORRECT_GUESS}\n"
                )
        elif self._game_state == GameState.ACTIVE:

            if isinstance(guess, str):  # guess was a word
                prompt += f"{self._INCORRECT_GUESS} \n"

            prompt += (
                f"{self._secret_word.show_letters(self._guesses)}\n"
                # display guessed letters, in alphabetical order, removing spaces
                + f"Guesses: {''.join(sorted(self._guesses)).strip()}\n"
                + f"{self._GUESSES_REMAINING} {self.guesses_left}\n"
                + f"{self._GUESS_PROMPT}\n"
            )

        else:  # unsuccessful guess and no guesses left: game over
            if isinstance(guess, str):  # if guess was a word and wrong inform user
                prompt += f"{self._INCORRECT_GUESS}"

            prompt += (
                f"{self._secret_word.show_letters(self._guesses)}\n"
                # display previously guessed words
                + f"Guesses: {''.join(self._guesses).replace(' ', '')}\n"
                + f"Word: {self._secret_word.formatted_word}\n"
                + f"{self._OUT_OF_TURNS}"
            )

        return prompt

    def guess(self, guess=None):
        """
        Handle the different cases for guessing letters or words in a hangman game.
            - No Guess
            - Empty Guess
            - Letter Guess
                - Previously Guessed Letter
                - Newly Guessed Letter
            - Word Guess

        Update _game_state and output accordingly.

        Args:
          guess:
            a letter or word to be guessed

        Returns:
            str:
                user_prompt to be printed for user
        """

        user_prompt = ""

        if isinstance(guess, str) and len(guess) > 1:  # A word was guessed

            # add an empty guess to _guesses to show a guess was used
            self._guesses.append(" ")

            # format the submitted guess
            cleaned_guess = guess.strip().upper()

            # secret word was guessed, user wins
            if self._secret_word.check(cleaned_guess):
                self._game_state = GameState.WON
            else:  # The guess is incorrect
                if self.guesses_left <= 0:  # no more guesses, user loses
                    self._game_state = GameState.LOST

            # set the prompt for a word guess
            user_prompt = self._format_prompt(cleaned_guess)

        # New letter guess (i.e. not a previously guessed letter)
        elif (
            isinstance(guess, str)
            and len(guess) == 1
            and guess.upper() not in self._guesses
        ):

            # add to guesses since a new letter was guessed
            self._guesses.append(guess.upper())

            # All letters have been guessed, game is won
            if self._secret_word.check_letters(self._guesses):
                self._game_state = GameState.WON

            # All guesses used up, game lost
            elif self.guesses_left <= 0:
                self._game_state = GameState.LOST

            # set format without a word guess
            user_prompt = self._format_prompt()

        else:  # empty string guess or None guess, don't add to guesses
            user_prompt = self._format_prompt()

        return user_prompt

    # def save(self):
    #     """
    #     Converts game state to a dictionary and saves it as JSON to RESTORE_FILE_PATH
    #     """
        
    #     # TO DO
    #     # Convert object data to dictionary
    #     # store  self.__class.__name__ with "class_name" key will need to look it up
    #     # store list of guesses from _guesses with key "guesses"
    #     # store _max_turns with key "max_turns"
    #     # store the string word from the secret word with the "word" key

    #     # use the RESTORE_FILE_PATH to save the file using json.dump
    #     pass
    def save(self):
    
        game_data = {}
        game_data["class_name"] = self.__class__.__name__
        game_data["guesses"] = self._guesses
        game_data["max_turns"] = self._max_turns
        game_data["word"] = self._secret_word.word  # make sure HangmanWord has .word

        with open(self.RESTORE_FILE_PATH, "w") as save_file:
            json.dump(game_data, save_file)

    @classmethod
    def restore(cls):
        """
        Creates a new game object from game state JSON in RESTORE_FILE_PATH
        """

        try:
            with open(cls.RESTORE_FILE_PATH, "r") as restore_file:
                data = json.load(restore_file)

        except FileNotFoundError:
            sys.exit(1)

        # look game class_type in list of global varialbes
        class_type = globals()[data["class_name"]]

        # Use class_type in place of class_name to create new object
        # pass looked up data as arguments: word, max turns
        restored_game = class_type(data["word"], data["max_turns"])

        # once game object created restore guesses from dictionary
        restored_game._guesses = data["guesses"]

        # remove old file
        pathlib.Path.unlink(cls.RESTORE_FILE_PATH)

        return restored_game
