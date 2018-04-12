
def assert_args_and_return(retval, *args, **kwargs):
    """
    Given a return value and an arbitrary set of arguments, returns a callable which will return ``retval`` when called
    with arguments matching those specified here, otherwise will raise an ``AssertionError``.

    This is intended to be used as a ``Mock`` object's ``side_effect``, allowing a mocked function's return value to be
    speficied at the same time as the expected arguments. This is a very concise way of doing things for simple uses
    where the mocked function is only ever called once (or with one set of arguments) and also has the beneficial
    trait of raising an ``AssertionError`` at the actual offending call site when there is an argument mismatch,
    leading to easy debugging.

    >>> from unittest.mock import Mock
    >>> mymock = Mock()
    >>> mymock.side_effect = assert_args_and_return("two eggs", "two bottles", yards=50)
    >>> mymock("two bottles", yards=50)
    "two eggs"
    >>> mymock("two bottles", metres=50)
    Traceback (most recent call last):
        ...
    AssertionError
    """
    def _inner(*inner_args, **inner_kwargs):
        assert args == inner_args
        assert kwargs == inner_kwargs
        return retval
    return _inner


def assert_args_and_raise(e, *args, **kwargs):
    """
    See ``assert_args_and_return`` except when arguments match, raises ``Exception`` ``e``.
    """
    def _inner(*inner_args, **inner_kwargs):
        assert args == inner_args
        assert kwargs == inner_kwargs
        raise e
    return _inner
