import enum
import pathlib
import signal
import sys

from word_game import GameState, HangmanGame, WordGame, WordleGame


class GameType(enum.Enum):
    """Enumeration of available game types."""

    HANGMAN = "HANGMAN"
    WORDLE = "WORDLE"
    RESTORE = "RESTORE"


class GameRunner:
    """Manages the execution of word guessing games (Hangman and Wordle).

    Handles command line argument processing, game initialization, signal
    handling for graceful interruption, and the main game loop.

    Class Attributes:
        INVALID_RETURN_BASE (int):
            base to add to when generating failed exit code

    Attributes:
        game (WordGame): The current game instance (HangmanGame or WordleGame)
        game_type (GameType): Type of game being played
        turns (int | None): Number of turns allowed in the game
        word (str | None): The secret word for the game
    """

    INVALID_RETURN_BASE = 128

    def __init__(self):
        """Initialize the GameRunner by processing command line arguments
        Initializes the game, registers signal handlers
        """
        self.game_type, self.turns, self.word = self._process_args()
        self._initialize_game()  # sets up self.game

        # Register signal handler to handle ctrl-c
        signal.signal(signal.SIGINT, self._interrupt_handler)

    def _process_args(self) -> tuple[GameType, int | None, str | None]:
        """
        Processes command line arguments to determine the number of turns and the
        specified word.

        Returns:
            tuple:
                Contains game type (GameType enum), the number of turns,
                and a word to guess.
        """
        turns = None
        word = None

        # Previous game data exists ignore command arguments
        if pathlib.Path.is_file(WordGame.RESTORE_FILE_PATH):
            game_type = GameType.RESTORE

        else:  # no prior game data
            try:
                game_type_str = sys.argv[1]

            except IndexError:
                print("Please enter a game type")
                sys.exit("No game type specified")

            game_type_str = game_type_str.upper()

            # Validate and convert to enum
            try:
                game_type = GameType[game_type_str]
            except KeyError:
                raise ValueError("Please pick Wordle or Hangman to play")

            if game_type == GameType.WORDLE:
                turns = 5
                try:
                    word = sys.argv[2]
                except IndexError:
                    word = None
            elif game_type == GameType.HANGMAN:
                try:
                    turns = int(sys.argv[2])

                except IndexError:
                    print("Please enter a number of turns")
                    sys.exit("No number of turns specified")

                try:
                    word = sys.argv[3]

                except IndexError:
                    word = None

        return game_type, turns, word

    def _interrupt_handler(self, signal_number: int, frame):
        """Handle interrupt signals (like Ctrl+C) by saving the game state.

        Args:
            signal_number (int): The signal number received
            frame: The current stack frame
        """
        print(f"\nCaught {signal_number} at line {frame.f_lineno} saving game")
        signal.signal(
            signal_number, signal.SIG_IGN
        )  # ignore additional signals so processing can finish

        if self.game:
            self.game.save()

        sys.exit(
            self.INVALID_RETURN_BASE + signal_number
        )  # https://stackoverflow.com/questions/1101957/are-there-any-standard-exit-status-codes-in-linux/1535733#1535733

    def _initialize_game(self):
        """Initialize the appropriate game type based on command line arguments."""
        if self.game_type == GameType.RESTORE:
            self.game = WordGame.restore()
        elif self.game_type == GameType.WORDLE:
            self.game = WordleGame(self.word)
        elif self.game_type == GameType.HANGMAN:
            self.game = HangmanGame(self.word, self.turns)

    def run(self):
        """
        Execute the main game loop, allowing the user to play until the
        game ends.

        Initializes the game, registers signal handlers, and processes
        user guesses until the game state changes from ACTIVE.
        """

        guess = ""
        while self.game.game_state == GameState.ACTIVE:
            prompt = self.game.guess(guess)
            print(prompt)
            guess = input("")


if __name__ == "__main__":
    runner = GameRunner()
    runner.run()
