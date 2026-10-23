from __future__ import annotations

from .. import types as t
from .._decoders import decode_quote
from .._params import NOT_GIVEN, NotGivenOr, body
from ._base import AsyncResource, Resource


class PayoutQuotes(Resource):
    def create(
        self,
        *,
        from_currency: str,
        to_currency: str,
        amount: str,
        payout_method: NotGivenOr[str | None] = NOT_GIVEN,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> t.PayoutQuote:
        """Quote a cross-currency payout. Pass its ``quote_id`` to ``payouts.create`` before it expires."""
        return self._transport.request(
            "POST",
            "/v1/payouts/quotes",
            decode_quote,
            body=body(from_currency=from_currency, to_currency=to_currency, amount=amount, payout_method=payout_method),
            has_body=True,
            idempotency_key=idempotency_key,
            timeout=timeout,
        )


class AsyncPayoutQuotes(AsyncResource):
    async def create(
        self,
        *,
        from_currency: str,
        to_currency: str,
        amount: str,
        payout_method: NotGivenOr[str | None] = NOT_GIVEN,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> t.PayoutQuote:
        """Quote a cross-currency payout. Pass its ``quote_id`` to ``payouts.create`` before it expires."""
        return await self._transport.request(
            "POST",
            "/v1/payouts/quotes",
            decode_quote,
            body=body(from_currency=from_currency, to_currency=to_currency, amount=amount, payout_method=payout_method),
            has_body=True,
            idempotency_key=idempotency_key,
            timeout=timeout,
        )
