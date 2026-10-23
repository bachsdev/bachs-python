"""Static fixtures, checked by mypy and never run. Each ignore marks an expected error, like @ts-expect-error."""

from werkzeug.datastructures import Headers

from bachs import Bachs, webhooks

bachs = Bachs(api_key="sk_sandbox_synthetic")
bachs.checkout_sessions.create(
    product_cart=[{"product_id": "prod_synthetic"}],
    customer={"email": "synthetic@example.com", "name": "Synthetic"},
)
bachs.checkout_sessions.create(pricing={"currency": "USD", "amount": "12.00"}, success_url="https://x.example")
bachs.checkout_sessions.create(pricing={"currency": "USD"}, cancel_url=None, customer=None)
bachs.subscriptions.cancel("sub_synthetic", cancel_at_period_end=True)
bachs.subscriptions.cancel("sub_synthetic", cancel_at_period_end=False, reason="Fraud")
bachs.subscriptions.cancel("sub_synthetic")
bachs.payouts.create(destination="pd_synthetic", amount="1.00")
bachs.payouts.create(destination="pd_synthetic", quote_id="pqt_synthetic", reference="ref", metadata=None)
bachs.payouts.list(limit=10, status_filter="completed")
bachs.payout_destinations.create(currency="NGN", account_number="0000000000", bank_code="001", label=None)
bachs.banks.resolve_account(account_number="0000000000", bank_code="001")
webhooks.construct_event("{}", {}, "synthetic")
webhooks.construct_event("{}", Headers(), "synthetic")
# A list of pairs is not a header object.
webhooks.construct_event("{}", [("X-Bachs-Signature-V2", "t=1")], "synthetic")  # type: ignore[arg-type]
# Request fields are keyword-only; a positional body is not accepted.
bachs.payouts.create({"destination": "pd_synthetic", "amount": "1.00"})  # type: ignore[call-arg, arg-type]
# Deprecated return_url is not exposed.
bachs.checkout_sessions.create(pricing={"currency": "USD"}, return_url="https://example.com")  # type: ignore[call-arg]
# Connect request fields are outside V1.
bachs.checkout_sessions.create(pricing={"currency": "USD"}, transfer_data={"destination": "acct"})  # type: ignore[call-arg]
# Money remains a decimal string.
bachs.payouts.create(destination="pd_synthetic", amount=1)  # type: ignore[arg-type]
# A status filter is one of the documented values.
bachs.payouts.list(status_filter="done")  # type: ignore[arg-type]
# A required field cannot be left out.
bachs.payouts.create(amount="1.00")  # type: ignore[call-arg]
bachs.banks.resolve_account(account_number="0000000000")  # type: ignore[call-arg]
# Direct charge beta is excluded.
bachs.payments.create(amount="1.00")  # type: ignore[attr-defined]
# Write retry controls are excluded.
bachs.subscriptions.cancel("sub_synthetic", max_retries=2)  # type: ignore[call-arg]
# Exactly-one rules (amount or quote_id; product_cart or pricing) are checked at runtime with BachsConfigError,
# since optional keywords cannot express them statically. See tests/test_webhooks_and_reliability.py.
