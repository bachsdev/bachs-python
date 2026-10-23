from __future__ import annotations

from .. import types as t
from .._decoders import decode_product, decode_product_list
from .._params import NOT_GIVEN, NotGivenOr, body
from .._transport import id_path
from ._base import AsyncResource, Resource


class Products(Resource):
    def create(
        self,
        *,
        name: str,
        price: t.PriceInput,
        description: NotGivenOr[str | None] = NOT_GIVEN,
        metadata: NotGivenOr[dict[str, t.JsonValue] | None] = NOT_GIVEN,
        billing_cycle: NotGivenOr[t.SubscriptionCadence | None] = NOT_GIVEN,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> t.Product:
        """Create a product. ``price`` is a fixed, free or custom price."""
        return self._transport.request(
            "POST",
            "/v1/products",
            decode_product,
            body=body(name=name, price=price, description=description, metadata=metadata, billing_cycle=billing_cycle),
            has_body=True,
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    def get(self, product_id: str, *, timeout: float | None = None, max_retries: int | None = None) -> t.Product:
        return self._transport.request(
            "GET",
            "/v1/products/" + id_path(product_id, "product_id"),
            decode_product,
            timeout=timeout,
            max_retries=max_retries,
        )

    def list(
        self,
        *,
        limit: NotGivenOr[int] = NOT_GIVEN,
        cursor: NotGivenOr[str] = NOT_GIVEN,
        include_archived: NotGivenOr[bool] = NOT_GIVEN,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> t.ProductList:
        """One page of products, by cursor: pass ``pagination.next_cursor`` as ``cursor`` for the next page."""
        return self._transport.request(
            "GET",
            "/v1/products",
            decode_product_list,
            query=body(limit=limit, cursor=cursor, include_archived=include_archived),
            timeout=timeout,
            max_retries=max_retries,
        )


class AsyncProducts(AsyncResource):
    async def create(
        self,
        *,
        name: str,
        price: t.PriceInput,
        description: NotGivenOr[str | None] = NOT_GIVEN,
        metadata: NotGivenOr[dict[str, t.JsonValue] | None] = NOT_GIVEN,
        billing_cycle: NotGivenOr[t.SubscriptionCadence | None] = NOT_GIVEN,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> t.Product:
        """Create a product. ``price`` is a fixed, free or custom price."""
        return await self._transport.request(
            "POST",
            "/v1/products",
            decode_product,
            body=body(name=name, price=price, description=description, metadata=metadata, billing_cycle=billing_cycle),
            has_body=True,
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    async def get(self, product_id: str, *, timeout: float | None = None, max_retries: int | None = None) -> t.Product:
        return await self._transport.request(
            "GET",
            "/v1/products/" + id_path(product_id, "product_id"),
            decode_product,
            timeout=timeout,
            max_retries=max_retries,
        )

    async def list(
        self,
        *,
        limit: NotGivenOr[int] = NOT_GIVEN,
        cursor: NotGivenOr[str] = NOT_GIVEN,
        include_archived: NotGivenOr[bool] = NOT_GIVEN,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> t.ProductList:
        """One page of products, by cursor: pass ``pagination.next_cursor`` as ``cursor`` for the next page."""
        return await self._transport.request(
            "GET",
            "/v1/products",
            decode_product_list,
            query=body(limit=limit, cursor=cursor, include_archived=include_archived),
            timeout=timeout,
            max_retries=max_retries,
        )
