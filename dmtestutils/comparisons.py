from functools import lru_cache
import re
from typing.re import Pattern


class RestrictedAny:
    """
    Analogous to mock.ANY, this class takes an arbitrary callable in its constructor and the returned instance will
    appear to "equal" anything that produces a truthy result when passed as an argument to the ``condition`` callable.
    """
    def __init__(self, condition):
        self._condition = condition

    def __eq__(self, other):
        return self._condition(other)

    def __repr__(self):
        return f"{self.__class__.__name__}({self._condition})"

    def __hash__(self):
        return None


class AnySupersetOf(RestrictedAny):
    """
    Instance will appear to "equal" any dictionary-like object that is a "superset" of the the constructor-supplied
    ``subset_dict``, i.e. will ignore any keys present in the dictionary in question but missing from the reference
    dict.
    """
    def __init__(self, subset_dict):
        self._subset_dict = subset_dict
        super().__init__(lambda other: self._subset_dict == {k: v for k, v in other.items() if k in self._subset_dict})

    def __repr__(self):
        return f"{self.__class__.__name__}({self._subset_dict})"


class AnyStringMatching(RestrictedAny):
    """
    Instance will appear to "equal" any string that matches the constructor-supplied regex pattern
    """
    _cached_re_compile = staticmethod(lru_cache(maxsize=32)(re.compile))

    def __init__(self, *args, **kwargs):
        """
        Construct an instance which will equal any string matching the supplied regex pattern. Supports all arguments
        recognized by ``re.compile``, alternatively accepts an existing regex pattern object as a single argument.
        """
        self._regex = (
            args[0]
            if len(args) == 1 and isinstance(args[0], Pattern)
            else self._cached_re_compile(*args, **kwargs)
        )
        super().__init__(lambda other: isinstance(other, (str, bytes)) and bool(self._regex.match(other)))

    def __repr__(self):
        return f"{self.__class__.__name__}({self._regex})"
