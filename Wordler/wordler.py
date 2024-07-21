from pathlib import Path
import typing as tp
from pprint import pprint

from Wordler import strategy

ALL = frozenset((0, 1, 2, 3, 4))


class Character(tp.NamedTuple):
    name: str
    known_position: tp.Optional[int] = None
    invalid_positions: set[int] = set()

    @classmethod
    def from_result(cls, name: str, position: int, result: str) -> tp.Self:
        known_position = None
        invalid_positions = ALL

        if result == "y":
            invalid_positions = {position}
        elif result == "g":
            invalid_positions -= {position}
            known_position = position
        return cls(
            name=name,
            known_position=known_position,
            invalid_positions=invalid_positions,
        )

    def fits(self, word: str) -> bool:
        if self.known_position is not None:
            return word[self.known_position] == self.name
        for pos in self.invalid_positions:
            if word[pos] == self.name:
                return False
        # If invalid positions isn't ALL, it means the character is in the word, we just don't know
        # where.
        if self.invalid_positions != ALL:
            return self.name in word

        return True


def word_is_valid(word: str, known_characters: tp.Iterable[Character]) -> bool:
    return all(c.fits(word) for c in known_characters)


def get_words() -> tuple[str]:
    """Read and return the words file"""
    all_words_fp = Path(__file__).parent.parent / "words.txt"
    return all_words_fp.read_text().split("\n")


def main(argv=None):
    candidate_words = get_words()

    print(
        "Welcome to wordler. I will try to solve today's wordle. Please help by entering my guesses into wordle, and then tell me the colours of the results."
    )

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

        characters = []
        for i, (char, resp) in enumerate(zip(best_word, response)):
            characters.append(Character.from_result(name=char, position=i, result=resp))

        # Now filter candidates.
        new_candidates = []
        for w in candidate_words:
            if word_is_valid(w, characters):
                new_candidates.append(w)
        candidate_words = new_candidates
        print(f"{len(new_candidates) = }")

    # C = Character
    # chars = [
    # C("w", invalid_positions=ALL),
    # C("e", invalid_positions=ALL),
    # C("y", invalid_positions=ALL),
    # C("h", invalid_positions=ALL),
    # C("o", invalid_positions=ALL),
    # C("m", invalid_positions=ALL),
    # C("t", invalid_positions=ALL),
    # C("a", invalid_positions={2, 1, 0}),
    # C("r", invalid_positions={2, 3, 4}),
    # C("s", invalid_positions=ALL),
    # C("b", invalid_positions={0}),
    # ]

    # # Filter words.
    # new_candidates = []
    # for w in candidate_words:
    # if word_is_valid(w, chars):
    # new_candidates.append(w)

    # print(f"{len(new_candidates)} new candidates.")
    # pprint(new_candidates)


if __name__ == "__main__":
    main()
