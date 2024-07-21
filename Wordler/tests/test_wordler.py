from Wordler.wordler import Character, ALL


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
