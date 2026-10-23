# Changelog

## 2.0.0

The first release under the shared SDK foundations. Code written for 1.x needs changes in two places: how request fields are passed, and how responses are read.

- **Request fields are keyword arguments.** `bachs.payouts.create(destination="pd_123", amount="50.00")` instead of a dictionary. Leaving an optional field out sends nothing; passing `None` sends `null`. A field the method does not know is a `TypeError`. Nested values such as `price` and `product_cart` items stay dictionaries.
- **Responses are typed objects.** `payout.status` and `page.items[0].name` instead of `payout["status"]`. A declared field the API left out reads as `None`; fields this SDK version does not declare are still readable; `.to_dict()` returns the JSON as received. Dictionary access on responses is removed.
- **`environment` is optional.** It is detected from the key prefix (`sk_sandbox_` or `sk_live_`) and exposed as `bachs.environment`. If `environment` is given and contradicts the key, the client refuses to start with `BachsConfigError`. A key with an unrecognised prefix still needs `environment`.
- **Logging** through the standard `bachs` logger. Warnings for an unrecognised key prefix and an exhausted retry budget; info for the environment in use; debug for each request. The key, bodies, portal URLs and webhook secrets are never logged.
- **`list_all`** on `products`, `payments`, `subscriptions`, `payout_destinations` and `payouts`: an iterator (async with `AsyncBachs`) over every item that fetches each page as it is reached. `list` is unchanged.
- Identifiers of `.` or `..` are rejected before any request is sent (also released as 1.0.2).
- The release workflow builds with pinned tool versions.

## 1.0.2

- Identifiers of `.` or `..` are rejected with `BachsConfigError` before any request is sent. Previously they passed through URL encoding unchanged and resolved as path navigation, so `payouts.get("..")` requested `/v1` and `subscriptions.cancel(".")` sent `DELETE /v1/subscriptions`, each carrying the API key. Only an application that passed untrusted input as an identifier was affected.
- The release workflow builds with pinned tool versions.

## 1.0.1

- `webhooks.construct_event` accepts Flask's `request.headers` (Werkzeug headers) and other header objects with an `items()` method. 1.0.0 rejected them with `BachsConfigError`; dicts, Starlette/FastAPI and Django headers already worked.

## 1.0.0

First release of the official Bachs server-side Python SDK, ported from the TypeScript SDK `1.0.0`.

- Resources: products, checkout sessions, subscriptions, customer portal sessions, payments, balances, banks, payout destinations, payout quotes and payouts.
- Webhooks: `webhooks.construct_event` verifies `X-Bachs-Signature-V2` against the raw body, checks the timestamp tolerance, and accepts any valid `v1` signature during secret rotation.
- Writes are sent once. An uncertain outcome (a timeout or lost response) is reported as `outcome_unknown`, so the caller reconciles before retrying with the same idempotency key.
- `Bachs` (sync) and `AsyncBachs` (asyncio or trio) clients with identical methods, on `httpx`, typed with `TypedDict`. `AsyncBachs` enforces the timeout exactly and supports task cancellation. Requires Python 3.10 or later.

Not yet covered: customers, refunds, Connect (accounts and transfers), virtual accounts and disputes.

`0.0.1` on PyPI was a placeholder. Do not use it.
