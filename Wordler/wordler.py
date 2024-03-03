from pathlib import Path
import typing as tp
from pprint import pprint

ALL = frozenset((0, 1, 2, 3, 4))


class Character(tp.NamedTuple):
    name: str
    position: tp.Optional[int] = None
    invalid_positions: set[int] = set()

    def fits(self, word: str) -> bool:
        if self.position is not None:
            return word[self.position] == self.name
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


def main(argv=None):
    all_words_fp = Path(__file__).parent.parent / "words.txt"
    candidate_words = all_words_fp.read_text().split("\n")

    C = Character
    chars = [
        C("w", invalid_positions=ALL),
        C("e", invalid_positions=ALL),
        C("y", invalid_positions=ALL),
        C("h", invalid_positions=ALL),
        C("o", invalid_positions=ALL),
        C("m", invalid_positions=ALL),
        C("t", invalid_positions=ALL),
        C("a", invalid_positions={2, 1, 0}),
        C("r", invalid_positions={2, 3, 4}),
        C("s", invalid_positions=ALL),
        C("b", invalid_positions={0}),
    ]

    # Filter words.
    new_candidates = []
    for w in candidate_words:
        if word_is_valid(w, chars):
            new_candidates.append(w)

    print(f"{len(new_candidates)} new candidates.")
    pprint(new_candidates)


if __name__ == "__main__":
    main()
