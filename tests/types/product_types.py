"""Static fixtures, checked by mypy and never run. Each ignore marks an expected error, like @ts-expect-error."""

from bachs import Bachs
from bachs.types import PriceInput

fixed: PriceInput = {"currency": "USD", "amount": "12.00"}
free: PriceInput = {"currency": "USD", "price_type": "free", "amount": None}
custom: PriceInput = {"currency": "USD", "price_type": "custom", "preset_amount": "12.00", "minimum_amount": None}
additional: PriceInput = {
    "currency": "USD", "amount": "12.00", "currency_options": [{"currency": "NGN", "amount": "12000.00"}]
}
# The fixed branch requires an amount.
missing_amount: PriceInput = {"currency": "USD", "price_type": "fixed"}  # type: ignore[assignment, misc]
# Decimal money is a string; do not silently turn numbers into API amounts.
numeric_amount: PriceInput = {"currency": "USD", "amount": 1200}  # type: ignore[typeddict-item]
# The free branch excludes a priced amount.
priced_free: PriceInput = {"currency": "USD", "price_type": "free", "amount": "12.00"}  # type: ignore[assignment, misc]
# Custom amounts belong in preset_amount, not a non-null amount.
custom_amount: PriceInput = {"currency": "USD", "price_type": "custom", "amount": "12.00"}  # type: ignore[assignment, misc]
# A fixed currency option also requires its decimal-string amount.
missing_option: PriceInput = {"currency": "USD", "amount": "12.00", "currency_options": [{"currency": "NGN"}]}  # type: ignore[typeddict-item]
bachs = Bachs(api_key="synthetic-only", environment="sandbox")
bachs.products.create(name="Pro Plan", price=fixed, idempotency_key="catalog-pro-plan")
bachs.products.create(name="Free", price=free, description=None, billing_cycle={"interval": "month", "frequency": 1})
bachs.products.list(limit=50, cursor="c2", include_archived=True)
# A product needs a name and a price.
bachs.products.create(price=fixed)  # type: ignore[call-arg]
# The price is a typed shape, not a loose dictionary.
bachs.products.create(name="Pro Plan", price={"currency": "USD", "amount": 12})  # type: ignore[typeddict-item]
# Write options cannot enable automatic retries.
bachs.products.create(name="Pro Plan", price=fixed, max_retries=2)  # type: ignore[call-arg]
bachs.products.get("prod_example", max_retries=0)
# Environment selection is explicit.
Bachs(api_key="synthetic-only", environment="staging")  # type: ignore[arg-type]
