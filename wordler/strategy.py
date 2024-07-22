from collections import defaultdict


def get_letter_frequencies(words: tuple[str]) -> dict[str, dict[int, int]]:
    "return a dict from {letter: {position: count}}"
    character_counts = defaultdict(lambda: defaultdict(int))

    for word in words:
        for i, char in enumerate(word):
            character_counts[char][i] += 1
    return {k: dict(v) for k, v in character_counts.items()}


def word_score(word: str, character_frequencies: dict[str, dict[int, int]]) -> int:
    """A word's score is the sum of its character frequencies"""
    return sum(character_frequencies[c].get(i, 0) for i, c in enumerate(word))


def best_word(words: tuple[str]) -> str:
    """Find the best word"""
    # pick the word that eliminates the most words. Try to pick a word with the highest frequencies.
    # Give each word a score, which is the sum of it's letter frequencies.

    freqencies = get_letter_frequencies(words)
    return max(words, key=lambda w: word_score(w, freqencies))
