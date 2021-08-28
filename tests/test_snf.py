from sharksnfishes import Grid, Fish, Shark, SharksNFishes
import pytest


@pytest.mark.parametrize("width, height", ((1, 2), (2, 1)))
def test_two_square_grid(width, height):
    g = Grid(width, height)
    assert g.width == width
    assert g.height == height
    # with pytest.raises():
    #     assert g.add(Fish(length, width))


def test_shark_fish_movement_gridplacement():
    g = Grid(2, 1)
    f1 = Fish(0, 0)
    f2 = Fish(0, 1)
    g.add(f1)
    g.add(f2)
    assert f1 in g.values()
    assert f2 in g.values()
    assert f1 == g[(0, 0)]
    assert f2 == g[(0, 1)]


def test_shark_fish_movement_combos():
    # Two fishes
    snf = SharksNFishes(2, 1, 0, 2)
    assert isinstance(snf.grid[(0, 0)], Fish)
    assert isinstance(snf.grid[(1, 0)], Fish)
    f1 = snf.grid[(0, 0)]
    f2 = snf.grid[(1, 0)]
    snf.run_updates()
    assert snf.grid[(0, 0)] == f1
    assert snf.grid[(1, 0)] == f2
    # Two sharks
    snf = SharksNFishes(2, 1, 2, 0)
    assert isinstance(snf.grid[(0, 0)], Shark)
    assert isinstance(snf.grid[(1, 0)], Shark)
    s1 = snf.grid[(0, 0)]
    s2 = snf.grid[(1, 0)]
    snf.run_updates()
    assert snf.grid[(0, 0)] == s1
    assert snf.grid[(1, 0)] == s2
    # One Shark, one fish
    snf = SharksNFishes(2, 1, 1, 1)
    if isinstance(snf.grid[(0, 0)], Shark):
        assert isinstance(snf.grid[(1, 0)], Fish)
        f1 = snf.grid[(1, 0)]
        s1 = snf.grid[(0, 0)]
    else:
        assert isinstance(snf.grid[(0, 0)], Fish)
        assert isinstance(snf.grid[(1, 0)], Shark)
        f1 = snf.grid[(0, 0)]
        s1 = snf.grid[(1, 0)]
    print("DEBUG: {}".format(snf.grid.creature_counter()))
    snf.run_updates()
    print("DEBUG: {}".format(snf.grid.creature_counter()))
    assert snf.grid.creature_counter()["Shark"] == 1
    assert snf.grid.creature_counter()["Fish"] == 0
