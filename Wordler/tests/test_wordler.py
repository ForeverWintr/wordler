from Wordler.wordler import Character, ALL


def test_character_fits():
    a = Character("a", position=4)

    assert a.fits("zzzza")
    assert not a.fits("zzzzb")
    assert not a.fits("bazzz")

    b = Character("b", invalid_positions=ALL)
    assert not b.fits("bbbbb")
    assert b.fits("aaaaa")

    c = Character("c", invalid_positions={1, 3})
    assert c.fits("casdf")
    assert not c.fits("cczzz")
    assert not c.fits("abdce")
    assert c.fits("abcde")

    # If c is not in an invalid position but invalid positions aren't ALL, we need to check that C
    # is in the string.
    assert not c.fits("xxxxx")

