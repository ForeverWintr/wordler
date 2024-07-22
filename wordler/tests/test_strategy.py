from Wordler import strategy, wordler


def test_letter_freq() -> None:
    # How frequently does each letter appear in each position?
    f = strategy.get_letter_frequencies(["abcde", "aegji"])
    assert f == {
        "a": {0: 2},
        "b": {1: 1},
        "c": {2: 1},
        "d": {3: 1},
        "e": {4: 1, 1: 1},
        "g": {2: 1},
        "j": {3: 1},
        "i": {4: 1},
    }


def test_best_word() -> None:
    words = ("cat", "bat", "bot")
    # words = wordler.get_words()
    w = strategy.best_word(words)
    assert w == "bat"
