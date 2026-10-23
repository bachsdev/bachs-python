"""Environment detection from the key prefix, and logging through the ``bachs`` logger (foundations 5 and 6)."""

from __future__ import annotations

import logging

import httpx
import pytest
from conftest import Mock, json_response

from bachs import AsyncBachs, Bachs, BachsApiError, BachsConfigError

product = {"id": "prod_1", "name": "P", "price": {"currency": "USD", "price_type": "fixed", "amount": "1.00"}}


def test_environment_comes_from_the_key_and_a_contradiction_refuses_to_start(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.DEBUG, logger="bachs")
    assert Bachs(api_key="sk_sandbox_synthetic").environment == "sandbox"
    assert Bachs(api_key="sk_live_synthetic").environment == "production"
    assert Bachs(api_key="sk_live_synthetic", environment="production").environment == "production"
    assert AsyncBachs(api_key="sk_sandbox_synthetic").environment == "sandbox"
    assert Bachs(api_key="unknown_prefix_key", environment="sandbox").environment == "sandbox"
    with pytest.raises(BachsConfigError, match=r"sandbox key \(sk_sandbox_\)") as wrong:
        Bachs(api_key="sk_sandbox_synthetic", environment="production")
    assert "synthetic" not in str(wrong.value), "The error names the key type, never the key."
    with pytest.raises(BachsConfigError):
        Bachs(api_key="sk_live_synthetic", environment="sandbox")
    with pytest.raises(BachsConfigError, match="pass environment explicitly"):
        Bachs(api_key="unknown_prefix_key")
    with pytest.raises(BachsConfigError):
        Bachs(api_key="sk_live_synthetic", environment="staging")  # type: ignore[arg-type]
    messages = [(r.levelname, r.getMessage()) for r in caplog.records]
    assert messages == [
        ("INFO", "using sandbox (sk_sandbox_ key)."),
        ("INFO", "using production (sk_live_ key)."),
        ("INFO", "using production (sk_live_ key)."),
        ("INFO", "using sandbox (sk_sandbox_ key)."),
        ("WARNING", 'the API key prefix is not recognised; using environment "sandbox" as given.'),
    ], "The environment line is info; only an unrecognised prefix warns. A refused client logs nothing."
    assert not any("synthetic" in m for _, m in messages), "Log lines never carry the key."


def test_the_key_environment_check_still_applies_with_a_base_url() -> None:
    with pytest.raises(BachsConfigError):
        Bachs(api_key="sk_sandbox_synthetic", environment="production", base_url="http://localhost:1")
    assert Bachs(api_key="sk_live_synthetic", base_url="http://localhost:1").environment == "production"


def test_requests_log_at_debug_only_and_never_the_credential(mock: Mock, caplog: pytest.LogCaptureFixture) -> None:
    mock.responses = [json_response(product, 200, {"x-request-id": "req_synthetic"})]
    caplog.set_level(logging.WARNING, logger="bachs")
    mock.client().products.get("prod_1")
    assert caplog.records == [], "At warning level a normal client logs nothing."
    caplog.set_level(logging.DEBUG, logger="bachs")
    mock.responses = [json_response(product, 200, {"x-request-id": "req_synthetic"})]
    mock.client().products.get("prod_1")
    debug = [r.getMessage() for r in caplog.records if r.levelno == logging.DEBUG]
    assert len(debug) == 1
    assert debug[0].startswith("GET /v1/products/prod_1 -> 200 in ")
    assert debug[0].endswith("ms (attempt 1, request req_synthetic)")
    everything = " ".join(r.getMessage() for r in caplog.records)
    # The info line names the prefix (sk_sandbox_); the key itself and the Authorization header never appear.
    assert "sk_sandbox_synthetic" not in everything and "Bearer" not in everything


def test_an_exhausted_retry_budget_warns_once(mock: Mock, clock: object, caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.WARNING, logger="bachs")
    mock.responses = [json_response({"detail": "busy"}, 503)] * 3
    with pytest.raises(BachsApiError):
        mock.client().products.get("prod_1")
    warnings = [r.getMessage() for r in caplog.records if r.levelno == logging.WARNING]
    assert warnings == ["GET /v1/products/prod_1 failed with 503 after 3 attempts; retry budget used up."]


def test_the_logger_is_the_standard_bachs_logger_with_no_handler_of_its_own() -> None:
    logger = logging.getLogger("bachs")
    assert logger.handlers == [] and logger.propagate, "Applications attach handlers; the SDK adds none."
    httpx.Client().close()
