from __future__ import annotations

from .. import types as t
from .._decoders import decode_portal
from .._transport import id_path
from ._base import AsyncResource, Resource


class CustomerPortal(Resource):
    def create_session(
        self, customer_id: str, *, idempotency_key: str | None = None, timeout: float | None = None
    ) -> t.PortalSession:
        """A short-lived portal URL for this customer. It carries a credential: never log or share it."""
        return self._transport.request(
            "POST",
            "/v1/customers/" + id_path(customer_id, "customer_id") + "/portal-sessions",
            decode_portal,
            idempotency_key=idempotency_key,
            timeout=timeout,
        )


class AsyncCustomerPortal(AsyncResource):
    async def create_session(
        self, customer_id: str, *, idempotency_key: str | None = None, timeout: float | None = None
    ) -> t.PortalSession:
        """A short-lived portal URL for this customer. It carries a credential: never log or share it."""
        return await self._transport.request(
            "POST",
            "/v1/customers/" + id_path(customer_id, "customer_id") + "/portal-sessions",
            decode_portal,
            idempotency_key=idempotency_key,
            timeout=timeout,
        )
