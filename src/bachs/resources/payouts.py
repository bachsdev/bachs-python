from __future__ import annotations

from typing import Any

from .. import types as t
from .._decoders import decode_payout, decode_payouts
from .._errors import BachsConfigError
from .._params import NOT_GIVEN, NotGiven, NotGivenOr, body
from .._transport import id_path
from ._base import AsyncResource, Resource


def _non_empty(value: Any) -> bool:
    return isinstance(value, str) and value.strip() != ""


def _check(amount: Any, quote_id: Any) -> None:
    has_amount, has_quote = not isinstance(amount, NotGiven), not isinstance(quote_id, NotGiven)
    if has_amount == has_quote or (has_amount and not _non_empty(amount)) or (has_quote and not _non_empty(quote_id)):
        raise BachsConfigError("Supply exactly one non-empty amount or quote_id.")


class Payouts(Resource):
    def create(
        self,
        *,
        destination: str,
        amount: NotGivenOr[str] = NOT_GIVEN,
        quote_id: NotGivenOr[str] = NOT_GIVEN,
        reference: NotGivenOr[str | None] = NOT_GIVEN,
        metadata: NotGivenOr[dict[str, t.JsonValue] | None] = NOT_GIVEN,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> t.Payout:
        """Pay out from your balance. Supply exactly one of ``amount`` (same currency) or ``quote_id``."""
        _check(amount, quote_id)
        return self._transport.request(
            "POST",
            "/v1/payouts",
            decode_payout,
            body=body(
                destination=destination, amount=amount, quote_id=quote_id, reference=reference, metadata=metadata
            ),
            has_body=True,
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    def get(self, payout_id: str, *, timeout: float | None = None, max_retries: int | None = None) -> t.Payout:
        return self._transport.request(
            "GET",
            "/v1/payouts/" + id_path(payout_id, "payout_id"),
            decode_payout,
            timeout=timeout,
            max_retries=max_retries,
        )

    def list(
        self,
        *,
        limit: NotGivenOr[int] = NOT_GIVEN,
        offset: NotGivenOr[int] = NOT_GIVEN,
        status_filter: NotGivenOr[t.PayoutStatusFilter] = NOT_GIVEN,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> t.PayoutList:
        """One page of payouts, by ``limit`` and ``offset``."""
        return self._transport.request(
            "GET",
            "/v1/payouts",
            decode_payouts,
            query=body(limit=limit, offset=offset, status_filter=status_filter),
            timeout=timeout,
            max_retries=max_retries,
        )


class AsyncPayouts(AsyncResource):
    async def create(
        self,
        *,
        destination: str,
        amount: NotGivenOr[str] = NOT_GIVEN,
        quote_id: NotGivenOr[str] = NOT_GIVEN,
        reference: NotGivenOr[str | None] = NOT_GIVEN,
        metadata: NotGivenOr[dict[str, t.JsonValue] | None] = NOT_GIVEN,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> t.Payout:
        """Pay out from your balance. Supply exactly one of ``amount`` (same currency) or ``quote_id``."""
        _check(amount, quote_id)
        return await self._transport.request(
            "POST",
            "/v1/payouts",
            decode_payout,
            body=body(
                destination=destination, amount=amount, quote_id=quote_id, reference=reference, metadata=metadata
            ),
            has_body=True,
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    async def get(self, payout_id: str, *, timeout: float | None = None, max_retries: int | None = None) -> t.Payout:
        return await self._transport.request(
            "GET",
            "/v1/payouts/" + id_path(payout_id, "payout_id"),
            decode_payout,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def list(
        self,
        *,
        limit: NotGivenOr[int] = NOT_GIVEN,
        offset: NotGivenOr[int] = NOT_GIVEN,
        status_filter: NotGivenOr[t.PayoutStatusFilter] = NOT_GIVEN,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> t.PayoutList:
        """One page of payouts, by ``limit`` and ``offset``."""
        return await self._transport.request(
            "GET",
            "/v1/payouts",
            decode_payouts,
            query=body(limit=limit, offset=offset, status_filter=status_filter),
            timeout=timeout,
            max_retries=max_retries,
        )
