from pyteal import compileTeal, Mode
import pytest

from .factorizer_game import logicsig, create


def test_create():
    # as int's:
    create(1, 2, 3)
    create(1, 0, 3)

    with pytest.raises(ValueError) as ae:
        create(1.1, 2.2, 3.3)

    with pytest.raises(ValueError) as ae:
        create(1.1, 2, 3)

    with pytest.raises(ValueError) as ae:
        create(1, 2.2, 3)

    with pytest.raises(ValueError) as ae:
        create(1, 2, 3.3)

    with pytest.raises(AssertionError) as ae:
        create(1, 2, 2)

    with pytest.raises(AssertionError) as ae:
        create(0, 2, 3)

    with pytest.raises(AssertionError) as ae:
        create(1, 2, -3)

    with pytest.raises(AssertionError) as ae:
        create(1, -2, 3)

    with pytest.raises(AssertionError) as ae:
        create(-1, 2, 3)

    # as str's:
    create("1", "2", "3")
    create("1", "0", "3")

    with pytest.raises(ValueError) as ae:
        create("1.1", "2.2", "3.3")

    with pytest.raises(ValueError) as ae:
        create("1.1", "2", "3")

    with pytest.raises(ValueError) as ae:
        create("1", "2.2", "3")

    with pytest.raises(ValueError) as ae:
        create("1", "2", "3.3")

    with pytest.raises(AssertionError) as ae:
        create("1", "2", "2")

    with pytest.raises(AssertionError) as ae:
        create("0", "2", "3")

    with pytest.raises(AssertionError) as ae:
        create("1", "2", "-3")

    with pytest.raises(AssertionError) as ae:
        create("1", "-2", "3")

    with pytest.raises(AssertionError) as ae:
        create("-1", "2", "3")


def test_validation():
    logicsig(1, 2, 3)
    logicsig(1, 0, 3)

    with pytest.raises(AssertionError) as ae:
        logicsig(1.1, 2.2, 3.3)

    with pytest.raises(AssertionError) as ae:
        logicsig(1.1, 2, 3)

    with pytest.raises(AssertionError) as ae:
        logicsig(1, 2.2, 3)

    with pytest.raises(AssertionError) as ae:
        logicsig(1, 2, 3.3)

    with pytest.raises(AssertionError) as ae:
        logicsig(1, 2, 2)

    with pytest.raises(AssertionError) as ae:
        logicsig(0, 2, 3)

    with pytest.raises(AssertionError) as ae:
        logicsig(1, 2, -3)

    with pytest.raises(AssertionError) as ae:
        logicsig(1, -2, 3)

    with pytest.raises(AssertionError) as ae:
        logicsig(-1, 2, 3)


def test_compile():
    x = compileTeal(create(1, 2, 3), Mode.Signature, version=5, assembleConstants=True)
    y = compileTeal(
        create("1", "2", "3"), Mode.Signature, version=5, assembleConstants=True
    )
    assert x == y
