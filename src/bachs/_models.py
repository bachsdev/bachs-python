"""Typed response objects: attribute access over the JSON Bachs returned, with every field retained."""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from typing import TYPE_CHECKING, Any, ClassVar, TypeVar, get_args, get_origin, get_type_hints

T = TypeVar("T", bound="Model")


class Model:
    """A response object. ``response.field`` reads a field; fields the SDK does not know yet are kept too.

    Subclasses declare their fields as annotations, so editors and type checkers know them. Nested
    annotations that name a ``Model`` subclass are wrapped on access, so ``checkout.charge.amount`` works.
    A declared field the API left out reads as ``None``. ``to_dict()`` returns the JSON exactly as received.
    """

    __slots__ = ("_data",)
    _data: dict[str, Any]
    _nested: ClassVar[dict[str, type[Model]]]
    _nested_lists: ClassVar[dict[str, type[Model]]]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        cls._nested = {}
        cls._nested_lists = {}
        for name, hint in get_type_hints(cls).items():
            if name.startswith("_"):
                continue
            item = _list_item_model(hint)
            if item is not None:
                cls._nested_lists[name] = item
                continue
            model = _model_in(hint)
            if model is not None:
                cls._nested[name] = model

    def __init__(self, data: Mapping[str, Any]) -> None:
        object.__setattr__(self, "_data", dict(data))

    # Hidden from type checkers so that only declared fields type-check: ``payout.staus`` is a static error.
    # At runtime every field in the JSON is readable, including ones this SDK version does not declare.
    if not TYPE_CHECKING:

        def __getattr__(self, name: str) -> Any:
            return self._field(name)

    def _field(self, name: str) -> Any:
        # Only reached for names that are not slots or class attributes: the JSON fields.
        if name.startswith("_"):
            raise AttributeError(name)
        data = object.__getattribute__(self, "_data")
        if name in data:
            value = data[name]
            if value is None:
                return None
            model = type(self)._nested.get(name)
            if model is not None and isinstance(value, Mapping):
                return model(value)
            item = type(self)._nested_lists.get(name)
            if item is not None and isinstance(value, list):
                return [item(v) if isinstance(v, Mapping) else v for v in value]
            return value
        if name in type(self).__annotations__:
            return None
        raise AttributeError(f"{type(self).__name__} has no field {name!r}")

    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError(f"{type(self).__name__} is read-only; use to_dict() for a mutable copy")

    def __contains__(self, name: object) -> bool:
        return name in self._data

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Model):
            return type(other) is type(self) and other._data == self._data
        return NotImplemented

    def __hash__(self) -> int:
        return id(self)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self._data!r})"

    def to_dict(self) -> dict[str, Any]:
        """The response as received, including fields this SDK version does not declare. A fresh copy."""
        copy: dict[str, Any] = _copy(self._data)
        return copy

    @classmethod
    def _from(cls: type[T], data: Mapping[str, Any]) -> T:
        return cls(data)


def _model_in(hint: Any) -> type[Model] | None:
    """The Model subclass named by a type hint, looking through ``X | None`` and ``Optional[X]``."""
    if isinstance(hint, type) and issubclass(hint, Model):
        return hint
    if get_origin(hint) is list:
        return None
    for arg in get_args(hint):
        if isinstance(arg, type) and issubclass(arg, Model):
            return arg
    return None


def _list_item_model(hint: Any) -> type[Model] | None:
    """The Model subclass of a ``list[X]`` hint, looking through ``list[X] | None``."""
    for candidate in (hint, *get_args(hint)):
        if get_origin(candidate) is list and get_args(candidate):
            return _model_in(get_args(candidate)[0])
    return None


def _copy(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _copy(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_copy(v) for v in value]
    return value
