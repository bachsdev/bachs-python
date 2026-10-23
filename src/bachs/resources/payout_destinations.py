from __future__ import annotations

from .. import types as t
from .._decoders import decode_destination, decode_destinations
from .._transport import id_path
from ._base import AsyncResource, Resource


class PayoutDestinations(Resource):
    def create(
        self,
        params: t.CreatePayoutDestinationRequest,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> t.PayoutDestination:
        return self._transport.request(
            "POST", "/v1/payouts/destinations", decode_destination,
            body=params, has_body=True, idempotency_key=idempotency_key, timeout=timeout,
        )

    def get(
        self, destination_id: str, *, timeout: float | None = None, max_retries: int | None = None
    ) -> t.PayoutDestination:
        return self._transport.request(
            "GET", "/v1/payouts/destinations/" + id_path(destination_id, "destination_id"), decode_destination,
            timeout=timeout, max_retries=max_retries,
        )

    def list(
        self,
        params: t.PayoutDestinationListParams | None = None,
        *,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> t.PayoutDestinationList:
        return self._transport.request(
            "GET", "/v1/payouts/destinations", decode_destinations,
            query=params, timeout=timeout, max_retries=max_retries,
        )


class AsyncPayoutDestinations(AsyncResource):
    async def create(
        self,
        params: t.CreatePayoutDestinationRequest,
        *,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> t.PayoutDestination:
        return await self._transport.request(
            "POST", "/v1/payouts/destinations", decode_destination,
            body=params, has_body=True, idempotency_key=idempotency_key, timeout=timeout,
        )

    async def get(
        self, destination_id: str, *, timeout: float | None = None, max_retries: int | None = None
    ) -> t.PayoutDestination:
        return await self._transport.request(
            "GET", "/v1/payouts/destinations/" + id_path(destination_id, "destination_id"), decode_destination,
            timeout=timeout, max_retries=max_retries,
        )

    async def list(
        self,
        params: t.PayoutDestinationListParams | None = None,
        *,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> t.PayoutDestinationList:
        return await self._transport.request(
            "GET", "/v1/payouts/destinations", decode_destinations,
            query=params, timeout=timeout, max_retries=max_retries,
        )
