"""Walk every page of a list endpoint, fetching the next page only when the caller reaches it.

Products page by cursor; payments, subscriptions, payouts and destinations page by limit and offset, and
destinations put their items in ``destinations``. The iterators hide those differences.
"""

from __future__ import annotations

from collections.abc import AsyncIterator, Awaitable, Callable, Iterator
from typing import Any, TypeVar

from ._models import Model
from ._params import NOT_GIVEN, NotGiven

Item = TypeVar("Item", bound=Model)


def _items(page: Model, field: str) -> list[Any]:
    value = getattr(page, field)
    return list(value) if isinstance(value, list) else []


def _offset_done(page: Model, field: str, items: list[Any], offset: int, limit: Any) -> bool:
    """Stop when the server says so, the page came back short, or the total is reached. An empty page always stops."""
    pagination = getattr(page, "pagination", None)
    has_more = getattr(pagination, "has_more", None) if pagination is not None else None
    total = getattr(page, "total", None)
    if total is None and pagination is not None:
        total = getattr(pagination, "total", None)
    if not items or has_more is False:
        return True
    if not isinstance(limit, NotGiven) and len(items) < limit:
        return True
    return total is not None and offset + len(items) >= total


def cursor_pages(fetch: Callable[[Any], Model], field: str) -> Iterator[Any]:
    cursor: Any = NOT_GIVEN
    while True:
        page = fetch(cursor)
        yield from _items(page, field)
        pagination = getattr(page, "pagination", None)
        cursor = getattr(pagination, "next_cursor", None) if pagination is not None else None
        if not cursor:
            return


async def async_cursor_pages(fetch: Callable[[Any], Awaitable[Model]], field: str) -> AsyncIterator[Any]:
    cursor: Any = NOT_GIVEN
    while True:
        page = await fetch(cursor)
        for item in _items(page, field):
            yield item
        pagination = getattr(page, "pagination", None)
        cursor = getattr(pagination, "next_cursor", None) if pagination is not None else None
        if not cursor:
            return


def offset_pages(fetch: Callable[[int], Model], field: str, limit: Any) -> Iterator[Any]:
    offset = 0
    while True:
        page = fetch(offset)
        items = _items(page, field)
        yield from items
        if _offset_done(page, field, items, offset, limit):
            return
        offset += len(items)


async def async_offset_pages(fetch: Callable[[int], Awaitable[Model]], field: str, limit: Any) -> AsyncIterator[Any]:
    offset = 0
    while True:
        page = await fetch(offset)
        items = _items(page, field)
        for item in items:
            yield item
        if _offset_done(page, field, items, offset, limit):
            return
        offset += len(items)
