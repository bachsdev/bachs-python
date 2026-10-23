from __future__ import annotations

from .. import types as t
from .._decoders import decode_banks, decode_resolved_account
from ._base import AsyncResource, Resource


class Banks(Resource):
    def list(
        self, params: t.BankListParams | None = None, *, timeout: float | None = None, max_retries: int | None = None
    ) -> t.BankList:
        return self._transport.request(
            "GET", "/v1/reference/banks", decode_banks, query=params, timeout=timeout, max_retries=max_retries
        )

    def resolve_account(
        self, params: t.ResolveBankAccountRequest, *, idempotency_key: str | None = None, timeout: float | None = None
    ) -> t.ResolvedBankAccount:
        """Can return ``resolved: False`` with a message without an HTTP error."""
        return self._transport.request(
            "POST", "/v1/misc/bank-accounts/resolve", decode_resolved_account,
            body=params, has_body=True, idempotency_key=idempotency_key, timeout=timeout,
        )


class AsyncBanks(AsyncResource):
    async def list(
        self, params: t.BankListParams | None = None, *, timeout: float | None = None, max_retries: int | None = None
    ) -> t.BankList:
        return await self._transport.request(
            "GET", "/v1/reference/banks", decode_banks, query=params, timeout=timeout, max_retries=max_retries
        )

    async def resolve_account(
        self, params: t.ResolveBankAccountRequest, *, idempotency_key: str | None = None, timeout: float | None = None
    ) -> t.ResolvedBankAccount:
        """Can return ``resolved: False`` with a message without an HTTP error."""
        return await self._transport.request(
            "POST", "/v1/misc/bank-accounts/resolve", decode_resolved_account,
            body=params, has_body=True, idempotency_key=idempotency_key, timeout=timeout,
        )
