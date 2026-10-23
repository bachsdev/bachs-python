"""Typed response objects: attribute access, nested models, unknown fields, missing fields and to_dict()."""

from __future__ import annotations

import pytest

from bachs import Model, types
from bachs._decoders import decode_checkout, decode_product_list

checkout_json = {
    "checkout_id": "chk_1", "status": "completed", "amount": "12.00", "currency": "USD",
    "charge": {"payment_id": "pay_1", "status": "succeeded", "amount": "12.00", "currency": "USD",
               "created_at": "2026-10-03T12:00:00Z", "updated_at": "2026-10-03T12:01:00Z", "narration": "future"},
    "customer": None, "metadata": {"order": "o_1"}, "release_note": {"added": "later"},
}


def test_attribute_access_reaches_declared_nested_and_unknown_fields() -> None:
    checkout = decode_checkout(checkout_json)
    assert isinstance(checkout, types.CheckoutSession)
    assert checkout.checkout_id == "chk_1" and checkout.amount == "12.00"
    assert isinstance(checkout.charge, types.Payment) and checkout.charge.payment_id == "pay_1"
    assert checkout.charge.narration == "future", "Unknown fields inside nested objects stay readable."  # type: ignore[attr-defined]
    assert checkout.release_note == {"added": "later"}, "Unknown top-level fields stay readable."  # type: ignore[attr-defined]
    assert checkout.metadata == {"order": "o_1"}, "Free-form dictionaries are returned as dictionaries."


def test_missing_declared_fields_read_as_none_and_null_stays_none() -> None:
    checkout = decode_checkout(checkout_json)
    assert checkout.customer is None, "An explicit null is None."
    assert checkout.success_url is None, "A declared field the API left out is None, not an error."
    assert "success_url" not in checkout and "customer" in checkout, "Membership tells omitted from null."
    with pytest.raises(AttributeError):
        checkout.not_a_field  # type: ignore[attr-defined]  # noqa: B018


def test_lists_of_models_and_pagination() -> None:
    page = decode_product_list({
        "items": [{"id": "prod_1", "name": "A", "price": {"currency": "USD", "price_type": "fixed", "amount": "1.00"}},
                  {"id": "prod_2", "name": "B", "price": {"currency": "USD", "price_type": "free", "amount": "0.00"}}],
        "pagination": {"next_cursor": "c2", "has_more": True},
    })
    assert [p.id for p in page.items] == ["prod_1", "prod_2"]
    assert isinstance(page.items[0].price, types.Price) and page.items[1].price.price_type == "free"
    assert page.pagination.next_cursor == "c2" and page.pagination.total is None
    assert page.items[0].prices is None, "An absent list field is None, not an empty list."


def test_to_dict_returns_the_raw_json_as_a_fresh_copy() -> None:
    checkout = decode_checkout(checkout_json)
    raw = checkout.to_dict()
    assert raw == checkout_json
    raw["charge"]["amount"] = "0.00"
    assert checkout.charge is not None and checkout.charge.amount == "12.00", "Mutating the copy leaves the model."
    assert checkout.to_dict() == checkout_json


def test_models_are_read_only_comparable_and_printable() -> None:
    a, b = decode_checkout(checkout_json), decode_checkout(checkout_json)
    assert a == b and a != checkout_json and a != types.Payment(checkout_json)
    with pytest.raises(AttributeError):
        a.status = "open"  # type: ignore[misc]
    assert repr(a).startswith("CheckoutSession({") and "chk_1" in repr(a)
    assert sorted(a) == sorted(checkout_json), "Iterating a model yields the field names present."
    assert issubclass(types.CheckoutSession, Model)


def test_secrets_are_not_special_cased_but_repr_is_the_raw_data() -> None:
    # A portal URL carries a credential; repr() shows it like any field, so callers must not log models wholesale.
    session = types.PortalSession({"id": "psn_1", "url": "https://portal.example.com/s/secret"})
    assert session.url.endswith("secret") and "secret" in repr(session)
