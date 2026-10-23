from __future__ import annotations

from collections.abc import AsyncIterator, Iterator

from .. import types as t
from .._decoders import decode_payment, decode_payments
from .._pagination import async_offset_pages, offset_pages
from .._params import NOT_GIVEN, NotGivenOr, body
from .._transport import id_path
from ._base import AsyncResource, Resource


class Payments(Resource):
    def get(self, payment_id: str, *, timeout: float | None = None, max_retries: int | None = None) -> t.Payment:
        return self._transport.request(
            "GET",
            "/v1/payments/" + id_path(payment_id, "payment_id"),
            decode_payment,
            timeout=timeout,
            max_retries=max_retries,
        )

    def list(
        self,
        *,
        limit: NotGivenOr[int] = NOT_GIVEN,
        offset: NotGivenOr[int] = NOT_GIVEN,
        status_filter: NotGivenOr[t.PaymentStatusFilter] = NOT_GIVEN,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> t.PaymentList:
        """One page of payments, by ``limit`` and ``offset``."""
        return self._transport.request(
            "GET",
            "/v1/payments",
            decode_payments,
            query=body(limit=limit, offset=offset, status_filter=status_filter),
            timeout=timeout,
            max_retries=max_retries,
        )

    def list_all(
        self,
        *,
        status_filter: NotGivenOr[t.PaymentStatusFilter] = NOT_GIVEN,
        limit: NotGivenOr[int] = NOT_GIVEN,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Iterator[t.PaymentListItem]:
        """Every item, one at a time, fetching each page only when it is reached."""

        def fetch(offset: int) -> t.PaymentList:
            return self.list(
                limit=limit, offset=offset, status_filter=status_filter, timeout=timeout, max_retries=max_retries
            )

        return offset_pages(fetch, "items", limit)


class AsyncPayments(AsyncResource):
    async def get(self, payment_id: str, *, timeout: float | None = None, max_retries: int | None = None) -> t.Payment:
        return await self._transport.request(
            "GET",
            "/v1/payments/" + id_path(payment_id, "payment_id"),
            decode_payment,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def list(
        self,
        *,
        limit: NotGivenOr[int] = NOT_GIVEN,
        offset: NotGivenOr[int] = NOT_GIVEN,
        status_filter: NotGivenOr[t.PaymentStatusFilter] = NOT_GIVEN,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> t.PaymentList:
        """One page of payments, by ``limit`` and ``offset``."""
        return await self._transport.request(
            "GET",
            "/v1/payments",
            decode_payments,
            query=body(limit=limit, offset=offset, status_filter=status_filter),
            timeout=timeout,
            max_retries=max_retries,
        )

    def list_all(
        self,
        *,
        status_filter: NotGivenOr[t.PaymentStatusFilter] = NOT_GIVEN,
        limit: NotGivenOr[int] = NOT_GIVEN,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> AsyncIterator[t.PaymentListItem]:
        """Every item, one at a time, fetching each page only when it is reached."""

        async def fetch(offset: int) -> t.PaymentList:
            return await self.list(
                limit=limit, offset=offset, status_filter=status_filter, timeout=timeout, max_retries=max_retries
            )

        return async_offset_pages(fetch, "items", limit)
