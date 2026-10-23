"""list_all walks cursor and offset pages lazily, hides the destinations envelope, and never loops (foundations 8)."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import httpx
import pytest
from conftest import KEY

from bachs import AsyncBachs, Bachs

pytestmark = pytest.mark.anyio


def product(i: int) -> dict[str, Any]:
    return {"id": f"prod_{i}", "name": f"P{i}", "price": {"currency": "USD", "price_type": "fixed", "amount": "1.00"}}


def payout(i: int) -> dict[str, Any]:
    return {"id": f"po_{i}", "status": "completed", "amount": "1.00", "currency": "USD"}


def destination(i: int) -> dict[str, Any]:
    return {"id": f"pd_{i}", "name": "D", "type": "bank_account", "currency": "NGN", "status": "approved"}


class FakeApi:
    """Answers list requests the way the Bachs API pages: products by cursor, the rest by limit and offset."""

    def __init__(self) -> None:
        self.calls: list[str] = []
        self.ignore_offset = False

    def __call__(self, request: httpx.Request) -> httpx.Response:
        url = request.url
        self.calls.append(url.path + ("?" + url.query.decode() if url.query else ""))
        q = url.params
        limit = int(q.get("limit", "50"))
        if url.path == "/v1/products":
            second = q.get("cursor") == "c2"
            items = [product(3), product(4)] if second else [product(1), product(2)]
            return httpx.Response(200, json={"items": items, "pagination": {"next_cursor": None if second else "c2"}})
        if url.path == "/v1/payouts":
            offset = 0 if self.ignore_offset else int(q.get("offset", "0"))
            items = [payout(offset + i) for i in range(min(limit, 5 - offset))]
            return httpx.Response(200, json={"total": 5, "items": items})
        if url.path == "/v1/payouts/destinations":
            offset = int(q.get("offset", "0"))
            items = [destination(0), destination(1)] if offset == 0 else [destination(2)]
            return httpx.Response(200, json={"destinations": items, "total": 3, "limit": limit, "offset": offset})
        if url.path == "/v1/subscriptions":
            return httpx.Response(200, json={"items": [], "pagination": {"has_more": False}})
        if url.path == "/v1/payments":
            offset = int(q.get("offset", "0"))
            items = [] if offset else [{"id": "pay_1", "status": "succeeded", "amount": "1", "currency": "USD",
                                        "customer_name": "n", "customer_email": "e"}]
            pagination = {"has_more": not offset, "limit": limit, "offset": offset, "returned": len(items), "total": 1}
            return httpx.Response(200, json={"items": items, "pagination": pagination})
        raise AssertionError(url.path)


@pytest.fixture
def api() -> FakeApi:
    return FakeApi()


def ids(iterator: Iterator[Any]) -> list[str]:
    return [item.id for item in iterator]


def test_list_all_walks_both_paging_styles_and_the_destinations_envelope(api: FakeApi) -> None:
    sdk = Bachs(api_key=KEY, http_client=httpx.Client(transport=httpx.MockTransport(api)), max_retries=0)
    assert ids(sdk.products.list_all(limit=2)) == ["prod_1", "prod_2", "prod_3", "prod_4"]
    assert api.calls == ["/v1/products?limit=2", "/v1/products?limit=2&cursor=c2"]
    api.calls.clear()
    assert ids(sdk.payouts.list_all(limit=2)) == ["po_0", "po_1", "po_2", "po_3", "po_4"]
    assert api.calls == ["/v1/payouts?limit=2&offset=0", "/v1/payouts?limit=2&offset=2", "/v1/payouts?limit=2&offset=4"]
    api.calls.clear()
    assert ids(sdk.payout_destinations.list_all(limit=2)) == ["pd_0", "pd_1", "pd_2"]
    assert ids(sdk.subscriptions.list_all()) == []
    assert ids(sdk.payments.list_all(status_filter="succeeded")) == ["pay_1"], "has_more False stops after one page."
    assert len(api.calls) == 2 + 1 + 1


def test_list_all_is_lazy_and_never_loops_on_a_server_that_ignores_offset(api: FakeApi) -> None:
    sdk = Bachs(api_key=KEY, http_client=httpx.Client(transport=httpx.MockTransport(api)), max_retries=0)
    first = next(iter(sdk.payouts.list_all(limit=2)))
    assert first.id == "po_0" and len(api.calls) == 1, "Only the first page is fetched until more is asked for."
    api.calls.clear()
    api.ignore_offset = True
    assert len(ids(sdk.payouts.list_all(limit=2))) == 6 and len(api.calls) == 3, "Stops at the total, no infinite loop."
    # list_all always starts from the first page: offset and cursor are not parameters at all.
    with pytest.raises(TypeError):
        sdk.payouts.list_all(offset=2)  # type: ignore[call-arg]
    with pytest.raises(TypeError):
        sdk.products.list_all(cursor="c2")  # type: ignore[call-arg]


async def test_async_list_all_matches_the_sync_iterator(api: FakeApi) -> None:
    sdk = AsyncBachs(api_key=KEY, http_client=httpx.AsyncClient(transport=httpx.MockTransport(api)), max_retries=0)
    assert [p.id async for p in sdk.products.list_all(limit=2)] == ["prod_1", "prod_2", "prod_3", "prod_4"]
    assert [p.id async for p in sdk.payouts.list_all(limit=2)] == ["po_0", "po_1", "po_2", "po_3", "po_4"]
    assert [d.id async for d in sdk.payout_destinations.list_all(limit=2)] == ["pd_0", "pd_1", "pd_2"]
    api.calls.clear()
    async for item in sdk.payouts.list_all(limit=2):
        assert item.id == "po_0"
        break
    assert len(api.calls) == 1
