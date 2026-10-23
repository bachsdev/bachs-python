from __future__ import annotations

from typing import Any

from .. import types as t
from .._decoders import decode_checkout, decode_checkout_created
from .._errors import BachsConfigError
from .._params import NOT_GIVEN, NotGiven, NotGivenOr, body
from .._transport import id_path
from ._base import AsyncResource, Resource


def _check(product_cart: Any, pricing: Any) -> None:
    has_cart, has_pricing = not isinstance(product_cart, NotGiven), not isinstance(pricing, NotGiven)
    if (
        has_cart == has_pricing
        or (has_cart and not isinstance(product_cart, list))
        or (has_pricing and not isinstance(pricing, dict))
    ):
        raise BachsConfigError("Supply exactly one of product_cart or pricing.")


class CheckoutSessions(Resource):
    def create(
        self,
        *,
        product_cart: NotGivenOr[list[t.CheckoutCartItem]] = NOT_GIVEN,
        pricing: NotGivenOr[t.CheckoutPricing] = NOT_GIVEN,
        customer: NotGivenOr[t.CustomerInput | None] = NOT_GIVEN,
        customer_creation: NotGivenOr[t.CustomerCreation] = NOT_GIVEN,
        billing_currency: NotGivenOr[str | None] = NOT_GIVEN,
        payment_method_types: NotGivenOr[list[t.PaymentMethodCorridor] | None] = NOT_GIVEN,
        success_url: NotGivenOr[str] = NOT_GIVEN,
        cancel_url: NotGivenOr[str | None] = NOT_GIVEN,
        reference: NotGivenOr[str | None] = NOT_GIVEN,
        metadata: NotGivenOr[dict[str, t.JsonValue] | None] = NOT_GIVEN,
        expires_in_minutes: NotGivenOr[int] = NOT_GIVEN,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> t.CheckoutSessionCreated:
        """Create a hosted checkout. Supply exactly one of ``product_cart`` or ``pricing`` (a raw amount)."""
        _check(product_cart, pricing)
        return self._transport.request(
            "POST",
            "/v1/checkout-sessions",
            decode_checkout_created,
            body=body(
                product_cart=product_cart,
                pricing=pricing,
                customer=customer,
                customer_creation=customer_creation,
                billing_currency=billing_currency,
                payment_method_types=payment_method_types,
                success_url=success_url,
                cancel_url=cancel_url,
                reference=reference,
                metadata=metadata,
                expires_in_minutes=expires_in_minutes,
            ),
            has_body=True,
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    def get(
        self, checkout_id: str, *, timeout: float | None = None, max_retries: int | None = None
    ) -> t.CheckoutSession:
        return self._transport.request(
            "GET",
            "/v1/checkout-sessions/" + id_path(checkout_id, "checkout_id"),
            decode_checkout,
            timeout=timeout,
            max_retries=max_retries,
        )


class AsyncCheckoutSessions(AsyncResource):
    async def create(
        self,
        *,
        product_cart: NotGivenOr[list[t.CheckoutCartItem]] = NOT_GIVEN,
        pricing: NotGivenOr[t.CheckoutPricing] = NOT_GIVEN,
        customer: NotGivenOr[t.CustomerInput | None] = NOT_GIVEN,
        customer_creation: NotGivenOr[t.CustomerCreation] = NOT_GIVEN,
        billing_currency: NotGivenOr[str | None] = NOT_GIVEN,
        payment_method_types: NotGivenOr[list[t.PaymentMethodCorridor] | None] = NOT_GIVEN,
        success_url: NotGivenOr[str] = NOT_GIVEN,
        cancel_url: NotGivenOr[str | None] = NOT_GIVEN,
        reference: NotGivenOr[str | None] = NOT_GIVEN,
        metadata: NotGivenOr[dict[str, t.JsonValue] | None] = NOT_GIVEN,
        expires_in_minutes: NotGivenOr[int] = NOT_GIVEN,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> t.CheckoutSessionCreated:
        """Create a hosted checkout. Supply exactly one of ``product_cart`` or ``pricing`` (a raw amount)."""
        _check(product_cart, pricing)
        return await self._transport.request(
            "POST",
            "/v1/checkout-sessions",
            decode_checkout_created,
            body=body(
                product_cart=product_cart,
                pricing=pricing,
                customer=customer,
                customer_creation=customer_creation,
                billing_currency=billing_currency,
                payment_method_types=payment_method_types,
                success_url=success_url,
                cancel_url=cancel_url,
                reference=reference,
                metadata=metadata,
                expires_in_minutes=expires_in_minutes,
            ),
            has_body=True,
            idempotency_key=idempotency_key,
            timeout=timeout,
        )

    async def get(
        self, checkout_id: str, *, timeout: float | None = None, max_retries: int | None = None
    ) -> t.CheckoutSession:
        return await self._transport.request(
            "GET",
            "/v1/checkout-sessions/" + id_path(checkout_id, "checkout_id"),
            decode_checkout,
            timeout=timeout,
            max_retries=max_retries,
        )
