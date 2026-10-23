"""Keyword-argument request bodies that keep "left out" and "None" distinct.

The Bachs API treats a missing field and ``null`` differently, so a method's keyword arguments default to
:data:`NOT_GIVEN`, and :func:`body` drops those before the request is serialised. Passing ``None`` sends ``null``.
"""

from __future__ import annotations

from typing import Any, Literal, TypeVar, Union, final

T = TypeVar("T")


@final
class NotGiven:
    """The default for an optional request field. Not the same as ``None``, which the API receives as ``null``."""

    __slots__ = ()

    def __bool__(self) -> Literal[False]:
        return False

    def __repr__(self) -> str:
        return "NOT_GIVEN"


NOT_GIVEN = NotGiven()
NotGivenOr = Union[T, NotGiven]


def body(**fields: Any) -> dict[str, Any]:
    """The request body: every keyword whose value was given, in the order declared."""
    return {name: value for name, value in fields.items() if not isinstance(value, NotGiven)}
