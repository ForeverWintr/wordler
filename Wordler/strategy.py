from collections import defaultdict, Counter

from Wordler.wordler import get_words


def get_letter_frequencies(words: tuple[str]) -> dict[str, dict[int, int]]:
    "return a dict from {letter: {position: count}}"
    character_counts = defaultdict(lambda: defaultdict(int))

    for word in words:
        for i, char in enumerate(word):
            character_counts[char][i] += 1
    return {k: dict(v) for k, v in character_counts.items()}
