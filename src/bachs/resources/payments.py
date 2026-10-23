from __future__ import annotations

from .. import types as t
from .._decoders import decode_payment, decode_payments
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
