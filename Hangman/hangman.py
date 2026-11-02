import random
from pathlib import Path

MAX_ATTEMPTS = 6
WORD_LIST_FILE = Path(__file__).with_name("google-10000-english-no-swears.txt")

# Used if words.txt is not present or contains no usable words.
FALLBACK_WORDS = [
    "python", "computer", "hangman", "keyboard", "planet",
    "garden", "library", "puzzle", "rainbow", "journey",
    "mountain", "notebook", "friendship", "sunshine", "elephant",
]

HANGMAN_STAGES = [
    r"""
     +---+
     |   |
         |
         |
         |
         |
    =========
""",
    r"""
     +---+
     |   |
     O   |
         |
         |
         |
    =========
""",
    r"""
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========
""",
    r"""
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========
""",
    r"""
     +---+
     |   |
     O   |
    /|\  |
         |
         |
    =========
""",
    r"""
     +---+
     |   |
     O   |
    /|\  |
    /    |
         |
    =========
""",
    r"""
     +---+
     |   |
     O   |
    /|\  |
    / \  |
         |
    =========
""",
]


def load_words():
    """Load words from words.txt, or use the built-in list."""
    if WORD_LIST_FILE.is_file():
        try:
            words = [
                line.strip().lower()
                for line in WORD_LIST_FILE.read_text(encoding="utf-8").splitlines()
                if line.strip().isalpha() and 4 <= len(line.strip()) <= 12
            ]
            if words:
                return words
        except OSError:
            pass

    return FALLBACK_WORDS


def display_game(secret_word, guessed_letters, wrong_guesses):
    """Show the gallows, masked word, and letters already guessed."""
    print(HANGMAN_STAGES[wrong_guesses])
    masked_word = " ".join(
        letter.upper() if letter in guessed_letters else "_"
        for letter in secret_word
    )
    print(f"Word: {masked_word}")
    print(f"Guessed letters: {' '.join(sorted(guessed_letters)).upper() or 'None'}")
    print(f"Attempts remaining: {MAX_ATTEMPTS - wrong_guesses}")


def get_guess(guessed_letters):
    """Ask until the player enters one new alphabetic letter."""
    while True:
        guess = input("\nGuess a letter: ").strip().lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Please enter exactly one letter (A-Z).")
        elif guess in guessed_letters:
            print(f"You already guessed '{guess.upper()}'. Try another letter.")
        else:
            return guess


def play_game():
    """Run one complete round of Hangman."""
    secret_word = random.choice(load_words())
    guessed_letters = set()
    wrong_guesses = 0

    print("\n" + "=" * 34)
    print("        H A N G M A N")
    print("=" * 34)
    print(f"Guess the hidden word. You have {MAX_ATTEMPTS} incorrect guesses.")

    while wrong_guesses < MAX_ATTEMPTS:
        display_game(secret_word, guessed_letters, wrong_guesses)

        if all(letter in guessed_letters for letter in secret_word):
            print("\n" + "=" * 34)
            print("          YOU WIN!")
            print(f"You guessed the word: {secret_word.upper()}")
            print("=" * 34)
            return

        guess = get_guess(guessed_letters)
        guessed_letters.add(guess)

        if guess in secret_word:
            print(f"Good guess! '{guess.upper()}' is in the word.")
        else:
            wrong_guesses += 1
            print(f"Sorry, '{guess.upper()}' is not in the word.")

    display_game(secret_word, guessed_letters, wrong_guesses)
    print("\n" + "=" * 34)
    print("          GAME OVER")
    print(f"The word was: {secret_word.upper()}")
    print("=" * 34)


def main():
    """Offer another round until the player chooses to quit."""
    while True:
        play_game()
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again not in {"y", "yes"}:
            print("\nThanks for playing Hangman. Goodbye!")
            break


if __name__ == "__main__":
    main()
