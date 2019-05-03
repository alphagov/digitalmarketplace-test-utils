from unittest.mock import Mock

import pytest

from dmtestutils.mocking import (
    assert_args_and_raise,
    assert_args_and_return,
    assert_args_and_return_or_raise,
    assert_args_and_return_iter_over,
)


class EggBottleException(Exception):
    pass


def test_assert_args_and_return():
    mymock = Mock()
    mymock.side_effect = assert_args_and_return("two eggs", "two bottles", yards=50)
    assert mymock('two bottles', yards=50) == "two eggs"

    with pytest.raises(AssertionError):
        mymock('two bottles', metres=50)


def test_assert_args_and_raise():
    mymock = Mock()

    mymock.side_effect = assert_args_and_raise(EggBottleException, "two bottles", yards=50)

    with pytest.raises(EggBottleException):
        mymock('two bottles', yards=50)

    with pytest.raises(AssertionError):
        mymock('two bottles', metres=50)


def test_assert_args_and_return_or_raise():
    mymock = Mock()
    mymock.side_effect = assert_args_and_return_or_raise("two eggs", EggBottleException, "two bottles", yards=50)

    assert mymock('two bottles', yards=50) == 'two eggs'

    with pytest.raises(EggBottleException):
        mymock('two bottles', metres=50)


def test_assert_args_and_return_iter_over():
    mymock = Mock()
    mymock.side_effect = assert_args_and_return_iter_over(("cocks", "aims", "pom", "pom",), "two bottles", yards=50)

    ret_iter_0 = mymock('two bottles', yards=50)

    assert next(ret_iter_0) == "cocks"
    assert next(ret_iter_0) == "aims"

    ret_iter_1 = mymock('two bottles', yards=50)

    assert next(ret_iter_1) == "cocks"

    assert tuple(ret_iter_0) == ("pom", "pom",)

    with pytest.raises(AssertionError):
        mymock('two battles', yards=50)
