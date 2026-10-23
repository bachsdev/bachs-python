from __future__ import annotations

from .. import types as t
from .._decoders import decode_banks, decode_resolved_account
from .._params import NOT_GIVEN, NotGivenOr, body
from ._base import AsyncResource, Resource


class Banks(Resource):
    def list(
        self, *, country: NotGivenOr[str] = NOT_GIVEN, timeout: float | None = None, max_retries: int | None = None
    ) -> t.BankList:
        return self._transport.request(
            "GET",
            "/v1/reference/banks",
            decode_banks,
            query=body(country=country),
            timeout=timeout,
            max_retries=max_retries,
        )

    def resolve_account(
        self,
        *,
        account_number: str,
        bank_code: str,
        country: NotGivenOr[str | None] = NOT_GIVEN,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> t.ResolvedBankAccount:
        """Look up an account name. Can return ``resolved=False`` with a message without an HTTP error."""
        return self._transport.request(
            "POST",
            "/v1/misc/bank-accounts/resolve",
            decode_resolved_account,
            body=body(account_number=account_number, bank_code=bank_code, country=country),
            has_body=True,
            idempotency_key=idempotency_key,
            timeout=timeout,
        )


class AsyncBanks(AsyncResource):
    async def list(
        self, *, country: NotGivenOr[str] = NOT_GIVEN, timeout: float | None = None, max_retries: int | None = None
    ) -> t.BankList:
        return await self._transport.request(
            "GET",
            "/v1/reference/banks",
            decode_banks,
            query=body(country=country),
            timeout=timeout,
            max_retries=max_retries,
        )

    async def resolve_account(
        self,
        *,
        account_number: str,
        bank_code: str,
        country: NotGivenOr[str | None] = NOT_GIVEN,
        idempotency_key: str | None = None,
        timeout: float | None = None,
    ) -> t.ResolvedBankAccount:
        """Look up an account name. Can return ``resolved=False`` with a message without an HTTP error."""
        return await self._transport.request(
            "POST",
            "/v1/misc/bank-accounts/resolve",
            decode_resolved_account,
            body=body(account_number=account_number, bank_code=bank_code, country=country),
            has_body=True,
            idempotency_key=idempotency_key,
            timeout=timeout,
        )
