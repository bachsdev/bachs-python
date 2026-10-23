from __future__ import annotations

from .. import types as t
from .._decoders import decode_quote
from ._base import AsyncResource, Resource


class PayoutQuotes(Resource):
    def create(
        self, params: t.CreatePayoutQuoteRequest, *, idempotency_key: str | None = None, timeout: float | None = None
    ) -> t.PayoutQuote:
        """A quote is not a payout. Pass its ``quote_id`` to ``payouts.create`` before it expires."""
        return self._transport.request(
            "POST", "/v1/payouts/quotes", decode_quote,
            body=params, has_body=True, idempotency_key=idempotency_key, timeout=timeout,
        )


class AsyncPayoutQuotes(AsyncResource):
    async def create(
        self, params: t.CreatePayoutQuoteRequest, *, idempotency_key: str | None = None, timeout: float | None = None
    ) -> t.PayoutQuote:
        """A quote is not a payout. Pass its ``quote_id`` to ``payouts.create`` before it expires."""
        return await self._transport.request(
            "POST", "/v1/payouts/quotes", decode_quote,
            body=params, has_body=True, idempotency_key=idempotency_key, timeout=timeout,
        )
