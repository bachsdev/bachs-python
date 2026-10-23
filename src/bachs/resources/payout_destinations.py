from __future__ import annotations

from collections.abc import AsyncIterator, Iterator

from .. import types as t
from .._decoders import decode_destination, decode_destinations
from .._pagination import async_offset_pages, offset_pages
from .._params import NOT_GIVEN, NotGivenOr, body
from .._transport import id_path
from ._base import AsyncResource, Resource


class PayoutDestinations(Resource):
    def create(
        self,
        *,
        currency: str,
        name: NotGivenOr[str | None] = NOT_GIVEN,
        label: NotGivenOr[str | None] = NOT_GIVEN,
        type: NotGivenOr[str | None] = NOT_GIVEN,
        destination_type: NotGivenOr[str | None] = NOT_GIVEN,
        account_number: NotGivenOr[str | None] = NOT_GIVEN,
        bank_code: NotGivenOr[str | None] = NOT_GIVEN,
        account_name: NotGivenOr[str | None] = NOT_GIVEN,
        bank_name: NotGivenOr[str | None] = NOT_GIVEN,
        phone_number: NotGivenOr[str | None] = NOT_GIVEN,
        mobile_provider: NotGivenOr[str | None] = NOT_GIVEN,
        wallet_address: NotGivenOr[str | None] = NOT_GIVEN,
        network: NotGivenOr[str | None] = NOT_GIVEN,
        metadata: NotGivenOr[dict[str, t.JsonValue] | None] = NOT_GIVEN,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> t.PayoutDestination:
        """Create a payout destination. Bachs reviews it; check ``is_usable`` before paying out to it."""
        return self._transport.request(
            "POST",
            "/v1/payouts/destinations",
            decode_destination,
            body=body(
                currency=currency,
                name=name,
                label=label,
                type=type,
                destination_type=destination_type,
                account_number=account_number,
                bank_code=bank_code,
                account_name=account_name,
                bank_name=bank_name,
                phone_number=phone_number,
                mobile_provider=mobile_provider,
                wallet_address=wallet_address,
                network=network,
                metadata=metadata,
            ),
            has_body=True,
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    def get(
        self, destination_id: str, *, timeout: float | None = None, max_retries: int | None = None
    ) -> t.PayoutDestination:
        return self._transport.request(
            "GET",
            "/v1/payouts/destinations/" + id_path(destination_id, "destination_id"),
            decode_destination,
            timeout=timeout,
            max_retries=max_retries,
        )

    def list(
        self,
        *,
        currency: NotGivenOr[str] = NOT_GIVEN,
        status: NotGivenOr[t.PayoutDestinationStatusFilter] = NOT_GIVEN,
        limit: NotGivenOr[int] = NOT_GIVEN,
        offset: NotGivenOr[int] = NOT_GIVEN,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> t.PayoutDestinationList:
        """One page of destinations, by ``limit`` and ``offset``. Items are in ``destinations``."""
        return self._transport.request(
            "GET",
            "/v1/payouts/destinations",
            decode_destinations,
            query=body(currency=currency, status=status, limit=limit, offset=offset),
            timeout=timeout,
            max_retries=max_retries,
        )

    def list_all(
        self,
        *,
        currency: NotGivenOr[str] = NOT_GIVEN,
        status: NotGivenOr[t.PayoutDestinationStatusFilter] = NOT_GIVEN,
        limit: NotGivenOr[int] = NOT_GIVEN,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Iterator[t.PayoutDestination]:
        """Every destination, one at a time, fetching each page only when it is reached."""

        def fetch(offset: int) -> t.PayoutDestinationList:
            return self.list(
                limit=limit, offset=offset, currency=currency, status=status, timeout=timeout, max_retries=max_retries
            )

        return offset_pages(fetch, "destinations", limit)


class AsyncPayoutDestinations(AsyncResource):
    async def create(
        self,
        *,
        currency: str,
        name: NotGivenOr[str | None] = NOT_GIVEN,
        label: NotGivenOr[str | None] = NOT_GIVEN,
        type: NotGivenOr[str | None] = NOT_GIVEN,
        destination_type: NotGivenOr[str | None] = NOT_GIVEN,
        account_number: NotGivenOr[str | None] = NOT_GIVEN,
        bank_code: NotGivenOr[str | None] = NOT_GIVEN,
        account_name: NotGivenOr[str | None] = NOT_GIVEN,
        bank_name: NotGivenOr[str | None] = NOT_GIVEN,
        phone_number: NotGivenOr[str | None] = NOT_GIVEN,
        mobile_provider: NotGivenOr[str | None] = NOT_GIVEN,
        wallet_address: NotGivenOr[str | None] = NOT_GIVEN,
        network: NotGivenOr[str | None] = NOT_GIVEN,
        metadata: NotGivenOr[dict[str, t.JsonValue] | None] = NOT_GIVEN,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> t.PayoutDestination:
        """Create a payout destination. Bachs reviews it; check ``is_usable`` before paying out to it."""
        return await self._transport.request(
            "POST",
            "/v1/payouts/destinations",
            decode_destination,
            body=body(
                currency=currency,
                name=name,
                label=label,
                type=type,
                destination_type=destination_type,
                account_number=account_number,
                bank_code=bank_code,
                account_name=account_name,
                bank_name=bank_name,
                phone_number=phone_number,
                mobile_provider=mobile_provider,
                wallet_address=wallet_address,
                network=network,
                metadata=metadata,
            ),
            has_body=True,
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    async def get(
        self, destination_id: str, *, timeout: float | None = None, max_retries: int | None = None
    ) -> t.PayoutDestination:
        return await self._transport.request(
            "GET",
            "/v1/payouts/destinations/" + id_path(destination_id, "destination_id"),
            decode_destination,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def list(
        self,
        *,
        currency: NotGivenOr[str] = NOT_GIVEN,
        status: NotGivenOr[t.PayoutDestinationStatusFilter] = NOT_GIVEN,
        limit: NotGivenOr[int] = NOT_GIVEN,
        offset: NotGivenOr[int] = NOT_GIVEN,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> t.PayoutDestinationList:
        """One page of destinations, by ``limit`` and ``offset``. Items are in ``destinations``."""
        return await self._transport.request(
            "GET",
            "/v1/payouts/destinations",
            decode_destinations,
            query=body(currency=currency, status=status, limit=limit, offset=offset),
            timeout=timeout,
            max_retries=max_retries,
        )

    def list_all(
        self,
        *,
        currency: NotGivenOr[str] = NOT_GIVEN,
        status: NotGivenOr[t.PayoutDestinationStatusFilter] = NOT_GIVEN,
        limit: NotGivenOr[int] = NOT_GIVEN,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> AsyncIterator[t.PayoutDestination]:
        """Every destination, one at a time, fetching each page only when it is reached."""

        async def fetch(offset: int) -> t.PayoutDestinationList:
            return await self.list(
                limit=limit, offset=offset, currency=currency, status=status, timeout=timeout, max_retries=max_retries
            )

        return async_offset_pages(fetch, "destinations", limit)
