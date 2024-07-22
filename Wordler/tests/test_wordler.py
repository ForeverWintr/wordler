from Wordler.wordler import (
    Character,
    ALL,
    evaluate_new_information,
    filter_words,
    get_words,
)
from Wordler import strategy


def test_character_fits():
    s = Character("s", known_at={0}, known_not_at={1, 2, 3, 4})
    a = Character("a", known_not_at={1})
    assert not s.fits("sanes")
    assert not a.fits("sanes")
    assert s.fits("scant")
    assert a.fits("scant")

    a = Character("a", known_at={4})

    assert a.fits("zzzza")
    assert not a.fits("zzzzb")
    assert not a.fits("bazzz")

    b = Character("b", known_not_at=set(ALL))
    assert not b.fits("bbbbb")
    assert b.fits("aaaaa")

    c = Character("c", known_not_at={1, 3})
    assert c.fits("casdf")
    assert not c.fits("cczzz")
    assert not c.fits("abdce")
    assert c.fits("abcde")

    # If c is not in an invalid position but invalid positions aren't ALL, we need to check that C
    # is in the string.
    assert not c.fits("xxxxx")


def test_character_update() -> None:
    # A is at position 0 and 3, but our guess had 3 'a's.
    c = Character("a")
    c.update(0, "g")
    c.update(1, "b")
    c.update(3, "g")

    assert c == Character("a", known_at={0, 3}, known_not_at={1, 2, 4})


def test_evaluate_new_information() -> None:
    characters = {}
    evaluate_new_information("scans", "gybbb", characters)

    assert characters == {
        "s": Character("s", known_at={0}, known_not_at={1, 2, 3, 4}),
        "c": Character("c", known_at=set(), known_not_at={1}),
        "a": Character("a", known_at=set(), known_not_at={0, 1, 2, 3, 4}),
        "n": Character("n", known_at=set(), known_not_at={0, 1, 2, 3, 4}),
    }


def test_filter_words() -> None:
    w = ["sanes", "atnes"]
    r = "byggg"
    characters = {}
    evaluate_new_information(w[0], r, characters)

    # This response rules out sanes.
    assert filter_words(w, characters.values()) == ["atnes"]


def test_crawl() -> None:
    # A manual unrolling of the loop.
    target = "crawl"

    candidate_words = get_words()
    characters = {}

    assert (best_word := strategy.best_word(candidate_words)) == "sanes"
    response = "bybbb"

    evaluate_new_information(
        word=best_word, user_response=response, characters=characters
    )

    # Now filter candidates.
    candidate_words = filter_words(candidate_words, characters=characters.values())
    assert target in candidate_words
    assert (best_word := strategy.best_word(candidate_words)) == "craal"
    response = "gggbg"

    evaluate_new_information(
        word=best_word, user_response=response, characters=characters
    )

    # Now filter candidates.
    candidate_words = filter_words(candidate_words, characters=characters.values())
    assert candidate_words == [target]
