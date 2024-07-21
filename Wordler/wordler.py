from pathlib import Path
import typing as tp
from pprint import pprint
from enum import Enum
from Wordler import strategy

ALL = frozenset((0, 1, 2, 3, 4))


class Classification(Enum):
    YELLOW = "y"
    GREEN = "g"
    BLACK = "b"


# Character can be in a known position, and subsequent characters can be yellow or black. A character can be in more than one position.
class Character:
    def __init__(
        self, name: str, known_at: set | None = None, known_not_at: set | None = None
    ):
        self.name = name
        self.known_at = known_at or set()
        self.known_not_at = known_not_at or set()

    def update(self, position: int, class_: Classification | str) -> None:
        """Update what we know about this character based on the user classification"""
        class_ = Classification(class_)

        if class_ is Classification.YELLOW:
            # This character is in the word, but not here.
            self.known_not_at.add(position)
            assert position not in self.known_at

        elif class_ is Classification.GREEN:
            # This character is at this position
            self.known_at.add(position)
            self.known_not_at.discard(position)

        elif class_ is Classification.BLACK:
            # This character is not in the word, UNLESS it's already green (or yellow?)
            # in a different position.
            self.known_not_at = set(ALL) - self.known_at

    def fits(self, word: str) -> bool:
        """Return true if this word is valid according to this character rule"""
        known_at_valid = all(word[p] == self.name for p in self.known_at)
        known_not_at_valid = all(word[p] != self.name for p in self.known_not_at)

        # We know the character is in the word if it's known to be at some but not all positions.
        in_word_valid = True
        if 0 < len(self.known_not_at) < 5:
            in_word_valid = self.name in word

        return known_at_valid and known_not_at_valid and in_word_valid

    def _key(self) -> tuple[str, set[int], set[int]]:
        return (self.name, self.known_at, self.known_not_at)

    def __eq__(self, other: tp.Any) -> bool | tp.Literal[NotImplemented]:
        try:
            return self._key() == other._key()
        except AttributeError:
            return NotImplemented

    def __repr__(self):
        return f"{type(self).__name__}({self.name!r}, known_at={self.known_at}, known_not_at={self.known_not_at})"


def filter_words(words: tuple[str], characters: tp.Sequence[Character]) -> tuple[str]:
    """Filter the words list based on the information we know about characters"""
    new_words = []
    for word in words:
        if all(c.fits(word) for c in characters):
            new_words.append(word)
    return new_words


def get_words() -> tuple[str]:
    """Read and return the words file"""
    all_words_fp = Path(__file__).parent.parent / "words.txt"
    return all_words_fp.read_text().split("\n")


def evaluate_new_information(
    word: str, user_response: str, characters: dict[str, Character]
) -> None:
    """Add new information to the characters dict based on the word and the new information from the user."""
    for i, (char, resp) in enumerate(zip(word, user_response)):
        character = characters.setdefault(char, Character(char))
        character.update(position=i, class_=resp)


def main(argv=None):
    candidate_words = get_words()

    print(
        "Welcome to wordler. I will try to solve today's wordle. Please help by entering my guesses into wordle, and then tell me the colours of the results."
    )

    characters = {}
    adj = "first"
    while True:
        best_word = strategy.best_word(candidate_words)
        probability = 1 / len(candidate_words)

        print()
        print(
            f"Here is my {adj} guess. I am {probability:.2%} sure this is the right word."
        )
        print(f"\n{best_word}\n")
        adj = "next"

        valid_input = False
        while not valid_input:
            response = input(
                f"Please type {best_word!r} into wordle, then enter the resulting colors, in order. [g]reen, [y]ellow, or [b]lack:\n"
            ).lower()
            if len(response) == 5 and all(c in {"g", "y", "b"} for c in response):
                valid_input = True
            else:
                print(
                    f"{response} isn't valid. Please enter exactly 5 characters, only using 'g', 'y', or 'b'."
                )

        evaluate_new_information(
            word=best_word, user_response=response, characters=characters
        )

        # Now filter candidates.
        candidate_words = filter_words(candidate_words, characters=characters.values())
        print(f"There are now {len(candidate_words)} candidate words")


if __name__ == "__main__":
    main()
