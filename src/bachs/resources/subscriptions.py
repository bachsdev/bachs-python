from __future__ import annotations

from collections.abc import AsyncIterator, Iterator

from .. import types as t
from .._decoders import decode_subscription, decode_subscriptions
from .._pagination import async_offset_pages, offset_pages
from .._params import NOT_GIVEN, NotGivenOr, body
from .._transport import id_path
from ._base import AsyncResource, Resource


class Subscriptions(Resource):
    def get(
        self, subscription_id: str, *, timeout: float | None = None, max_retries: int | None = None
    ) -> t.Subscription:
        return self._transport.request(
            "GET",
            "/v1/subscriptions/" + id_path(subscription_id, "subscription_id"),
            decode_subscription,
            timeout=timeout,
            max_retries=max_retries,
        )

    def list(
        self,
        *,
        limit: NotGivenOr[int] = NOT_GIVEN,
        offset: NotGivenOr[int] = NOT_GIVEN,
        customer_id: NotGivenOr[str] = NOT_GIVEN,
        status: NotGivenOr[t.SubscriptionStatusFilter] = NOT_GIVEN,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> t.SubscriptionList:
        """One page of subscriptions, by ``limit`` and ``offset``."""
        return self._transport.request(
            "GET",
            "/v1/subscriptions",
            decode_subscriptions,
            query=body(limit=limit, offset=offset, customer_id=customer_id, status=status),
            timeout=timeout,
            max_retries=max_retries,
        )

    def list_all(
        self,
        *,
        customer_id: NotGivenOr[str] = NOT_GIVEN,
        status: NotGivenOr[t.SubscriptionStatusFilter] = NOT_GIVEN,
        limit: NotGivenOr[int] = NOT_GIVEN,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> Iterator[t.Subscription]:
        """Every item, one at a time, fetching each page only when it is reached."""

        def fetch(offset: int) -> t.SubscriptionList:
            return self.list(
                limit=limit,
                offset=offset,
                customer_id=customer_id,
                status=status,
                timeout=timeout,
                max_retries=max_retries,
            )

        return offset_pages(fetch, "items", limit)

    def cancel(
        self,
        subscription_id: str,
        *,
        cancel_at_period_end: NotGivenOr[bool] = NOT_GIVEN,
        reason: NotGivenOr[str | None] = NOT_GIVEN,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> t.Subscription:
        """Cancel at the end of the paid period (``cancel_at_period_end=True``) or immediately (``False``)."""
        return self._transport.request(
            "DELETE",
            "/v1/subscriptions/" + id_path(subscription_id, "subscription_id"),
            decode_subscription,
            body=body(cancel_at_period_end=cancel_at_period_end, reason=reason),
            has_body=True,
            idempotency_key=idempotency_key,
            timeout=timeout,
        )


class AsyncSubscriptions(AsyncResource):
    async def get(
        self, subscription_id: str, *, timeout: float | None = None, max_retries: int | None = None
    ) -> t.Subscription:
        return await self._transport.request(
            "GET",
            "/v1/subscriptions/" + id_path(subscription_id, "subscription_id"),
            decode_subscription,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def list(
        self,
        *,
        limit: NotGivenOr[int] = NOT_GIVEN,
        offset: NotGivenOr[int] = NOT_GIVEN,
        customer_id: NotGivenOr[str] = NOT_GIVEN,
        status: NotGivenOr[t.SubscriptionStatusFilter] = NOT_GIVEN,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> t.SubscriptionList:
        """One page of subscriptions, by ``limit`` and ``offset``."""
        return await self._transport.request(
            "GET",
            "/v1/subscriptions",
            decode_subscriptions,
            query=body(limit=limit, offset=offset, customer_id=customer_id, status=status),
            timeout=timeout,
            max_retries=max_retries,
        )

    def list_all(
        self,
        *,
        customer_id: NotGivenOr[str] = NOT_GIVEN,
        status: NotGivenOr[t.SubscriptionStatusFilter] = NOT_GIVEN,
        limit: NotGivenOr[int] = NOT_GIVEN,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> AsyncIterator[t.Subscription]:
        """Every item, one at a time, fetching each page only when it is reached."""

        async def fetch(offset: int) -> t.SubscriptionList:
            return await self.list(
                limit=limit,
                offset=offset,
                customer_id=customer_id,
                status=status,
                timeout=timeout,
                max_retries=max_retries,
            )

        return async_offset_pages(fetch, "items", limit)

    async def cancel(
        self,
        subscription_id: str,
        *,
        cancel_at_period_end: NotGivenOr[bool] = NOT_GIVEN,
        reason: NotGivenOr[str | None] = NOT_GIVEN,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> t.Subscription:
        """Cancel at the end of the paid period (``cancel_at_period_end=True``) or immediately (``False``)."""
        return await self._transport.request(
            "DELETE",
            "/v1/subscriptions/" + id_path(subscription_id, "subscription_id"),
            decode_subscription,
            body=body(cancel_at_period_end=cancel_at_period_end, reason=reason),
            has_body=True,
            idempotency_key=idempotency_key,
            timeout=timeout,
        )
