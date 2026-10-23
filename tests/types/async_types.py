"""Static fixtures, checked by mypy and never run. Each ignore marks an expected error, like @ts-expect-error."""

import httpx
from typing_extensions import assert_type

from bachs import AsyncBachs
from bachs.types import Payout, ProductList


async def usage() -> None:
    async with AsyncBachs(api_key="synthetic", environment="sandbox", http_client=httpx.AsyncClient()) as bachs:
        payout = await bachs.payouts.create(destination="pd_x", amount="1.00")
        assert_type(payout, Payout)
        assert_type(payout.status, str)
        assert_type(payout.failure_reason, "str | None")
        page = await bachs.products.list(limit=1)
        assert_type(page, ProductList)
        assert_type(page.items[0].price.amount, str)
        # A misspelled field is a type error, not a runtime surprise.
        _typo = payout.staus  # type: ignore[attr-defined]
        # Results must be awaited before use.
        _unawaited = bachs.payouts.get("po_x").status  # type: ignore[attr-defined]
        # Write retry controls are excluded, as on the sync client.
        await bachs.payouts.create(destination="pd_x", amount="1.00", max_retries=2)  # type: ignore[call-arg]
        # Money remains a decimal string.
        await bachs.payouts.create(destination="pd_x", amount=1)  # type: ignore[arg-type]


# The async client takes an httpx.AsyncClient, not a sync one.
AsyncBachs(api_key="synthetic", environment="sandbox", http_client=httpx.Client())  # type: ignore[arg-type]
