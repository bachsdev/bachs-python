"""Request and response shapes. Fields keep Bachs snake_case and money stays in decimal strings.

Requests are ``TypedDict`` shapes. Responses are :class:`bachs.Model` objects: ``response.field`` reads a
field, a declared field the API left out reads as ``None``, fields this SDK version does not declare are
still readable, and ``to_dict()`` returns the JSON exactly as received.
"""

from __future__ import annotations

from typing import Any, Literal, TypeAlias, Union

from typing_extensions import NotRequired, TypedDict

from ._models import Model

JsonValue: TypeAlias = Union[None, bool, int, float, str, list["JsonValue"], dict[str, "JsonValue"]]

ProductCurrency = Literal["USD", "NGN", "GHS", "KES", "MWK", "RWF", "TZS", "UGX", "XAF", "XOF", "ZMW"]
PriceType = Literal["fixed", "free", "custom"]

# Products


class FixedCurrencyOptionInput(TypedDict):
    currency: ProductCurrency
    amount: str


class FreeCurrencyOptionInput(TypedDict):
    currency: ProductCurrency
    amount: NotRequired[None]


class CustomCurrencyOptionInput(TypedDict):
    currency: ProductCurrency
    amount: NotRequired[None]
    preset_amount: NotRequired[str | None]
    minimum_amount: NotRequired[str | None]
    maximum_amount: NotRequired[str | None]


class FixedPriceInput(TypedDict):
    currency: ProductCurrency
    price_type: NotRequired[Literal["fixed"]]
    amount: str
    currency_options: NotRequired[list[FixedCurrencyOptionInput] | None]


class FreePriceInput(TypedDict):
    currency: ProductCurrency
    price_type: Literal["free"]
    amount: NotRequired[None]
    currency_options: NotRequired[list[FreeCurrencyOptionInput] | None]


class CustomPriceInput(TypedDict):
    currency: ProductCurrency
    price_type: Literal["custom"]
    amount: NotRequired[None]
    preset_amount: NotRequired[str | None]
    minimum_amount: NotRequired[str | None]
    maximum_amount: NotRequired[str | None]
    currency_options: NotRequired[list[CustomCurrencyOptionInput] | None]


PriceInput = Union[FixedPriceInput, FreePriceInput, CustomPriceInput]


class SubscriptionCadence(TypedDict, total=False):
    """The published cadence schema does not specify a required-field list."""

    interval: Literal["day", "week", "month", "year"]
    frequency: int


class CreateProductRequest(TypedDict):
    name: str
    description: NotRequired[str | None]
    price: PriceInput
    metadata: NotRequired[dict[str, JsonValue] | None]
    billing_cycle: NotRequired[SubscriptionCadence | None]


class ProductListParams(TypedDict, total=False):
    limit: int
    cursor: str
    include_archived: bool


class CurrencyOption(Model):
    currency: str
    amount: str | None
    preset_amount: str | None
    minimum_amount: str | None
    maximum_amount: str | None


class Price(Model):
    currency: str
    price_type: PriceType
    amount: str
    preset_amount: str | None
    minimum_amount: str | None
    maximum_amount: str | None
    currency_options: list[CurrencyOption] | None


class ProductCurrencyPrice(Model):
    currency: str | None
    amount: str | None
    minimum_amount: str | None
    maximum_amount: str | None
    is_default: bool | None


class BillingCycle(Model):
    interval: Literal["day", "week", "month", "year"] | None
    frequency: int | None


class Product(Model):
    id: str
    name: str
    price: Price
    organization_id: str | None
    description: str | None
    status: str | None
    metadata: dict[str, Any] | None
    media: list[dict[str, Any]] | None
    actor_id: str | None
    created_at: str | None
    updated_at: str | None
    archived_at: str | None
    billing_cycle: BillingCycle | None
    prices: list[ProductCurrencyPrice] | None
    total_payments: float | None
    total_amount: str | None


class Pagination(Model):
    next_cursor: str | None
    prev_cursor: str | None
    has_more: bool | None
    limit: int | None
    offset: int | None
    returned: int | None
    total: int | None


class ProductList(Model):
    items: list[Product]
    pagination: Pagination


# Checkout sessions

PaymentMethodCorridor = Literal[
    "USD_CARD", "NGN_CARD", "NGN_BANK_TRANSFER", "MOMO_GHS", "MOMO_KES", "MOMO_TZS", "MOMO_UGX",
    "MOMO_XAF", "MOMO_XOF", "MOMO_RWF", "MOMO_MWK", "MOMO_ZMW", "CRYPTO",
]


class ExistingCustomerInput(TypedDict):
    customer_id: str


class NewCustomerInput(TypedDict):
    email: str
    name: str
    phone_number: NotRequired[str | None]


CustomerInput = Union[ExistingCustomerInput, NewCustomerInput]


class CheckoutPricing(TypedDict):
    currency: str
    amount: NotRequired[str]
    price_type: NotRequired[PriceType]
    preset_amount: NotRequired[str]
    minimum_amount: NotRequired[str]
    maximum_amount: NotRequired[str]
    currency_options: NotRequired[dict[str, str]]


class CartPriceOverride(TypedDict, total=False):
    price_type: PriceType
    amount: str | None
    preset_amount: str | None
    minimum_amount: str | None
    maximum_amount: str | None


class CheckoutCartItem(TypedDict):
    product_id: str
    quantity: NotRequired[int]
    amount: NotRequired[str | None]
    pricing: NotRequired[CartPriceOverride | None]


class _CheckoutCommonInput(TypedDict, total=False):
    customer: CustomerInput | None
    customer_creation: Literal["always", "if_required"]
    billing_currency: str | None
    payment_method_types: list[PaymentMethodCorridor] | None
    success_url: str
    cancel_url: str | None
    reference: str | None
    metadata: dict[str, JsonValue] | None
    expires_in_minutes: int


class CartCheckoutSessionRequest(_CheckoutCommonInput):
    product_cart: list[CheckoutCartItem]


class PricingCheckoutSessionRequest(_CheckoutCommonInput):
    pricing: CheckoutPricing


# Supply exactly one of product_cart or pricing.
CreateCheckoutSessionRequest = Union[CartCheckoutSessionRequest, PricingCheckoutSessionRequest]


class CheckoutSessionCreated(Model):
    checkout_id: str
    checkout_url: str
    status: str
    expires_at: str
    created_at: str
    reference: str | None


class CheckoutIdentity(Model):
    id: str | None
    email: str | None
    name: str | None


# Payments

PaymentStatusFilter = Literal[
    "created", "processing", "succeeded", "accepted", "failed", "expired", "cancelled", "refunded",
    "partially_refunded", "auto_refunded", "underpaid", "overpaid",
]


class Payment(Model):
    payment_id: str
    status: str
    amount: str
    currency: str
    created_at: str
    updated_at: str
    reference: str | None
    checkout_id: str | None
    subscription_id: str | None
    billing_reason: str | None
    fee_usd: str | None
    amount_paid: str | None
    amount_remaining: str | None
    payment_method: str | None
    completed_at: str | None
    is_refundable: bool | None
    meta: dict[str, Any] | None


class CheckoutSession(Model):
    checkout_id: str
    status: str
    amount: str | None
    currency: str | None
    payment_status: str | None
    source_type: str | None
    reference: str | None
    charge: Payment | None
    payment_method: str | None
    customer: CheckoutIdentity | None
    customer_details: CheckoutIdentity | None
    success_url: str | None
    cancel_url: str | None
    billing_currency: str | None
    session_mode: str | None
    metadata: dict[str, Any] | None
    created_at: str | None
    expires_at: str | None
    completed_at: str | None
    updated_at: str | None


class PaymentListItem(Model):
    id: str | None
    status: str
    amount: str
    currency: str
    customer_name: str
    customer_email: str
    reference: str | None
    amount_paid: str | None
    amount_remaining: str | None
    settlement_amount: str | None
    settlement_currency: str | None
    fee: str | None
    vat: str | None
    transaction_date: str | None
    completed_at: str | None


class PaymentListParams(TypedDict, total=False):
    limit: int
    offset: int
    status_filter: PaymentStatusFilter


class PaymentPagination(Model):
    has_more: bool
    limit: int
    offset: int
    returned: int
    total: int
    next_cursor: str | None
    prev_cursor: str | None


class PaymentList(Model):
    items: list[PaymentListItem]
    pagination: PaymentPagination


# Subscriptions and customer portal


class SubscriptionCustomer(Model):
    customer_id: str | None
    email: str | None
    name: str | None
    phone_number: str | None


class SubscriptionItem(Model):
    id: str | None
    status: str | None
    quantity: float | None
    recurring: bool | None
    price_type: str | None
    unit_amount: str | None
    currency: str | None
    previously_billed_at: str | None
    next_billed_at: str | None


class Subscription(Model):
    id: str
    status: str
    customer: SubscriptionCustomer | None
    payment_method_id: str | None
    collection_method: str | None
    currency: str | None
    amount: str | None
    billing_cycle: BillingCycle | None
    quantity: float | None
    current_period_start: str | None
    current_period_end: str | None
    previously_billed_at: str | None
    next_billed_at: str | None
    trial_end: str | None
    cancel_at_period_end: bool | None
    canceled_at: str | None
    created_at: str | None
    items: list[SubscriptionItem] | None
    metadata: dict[str, Any] | None


class SubscriptionListParams(TypedDict, total=False):
    limit: int
    offset: int
    customer_id: str
    status: Literal["trialing", "active", "past_due", "unpaid", "canceled"]


class SubscriptionList(Model):
    items: list[Subscription]
    pagination: Pagination


class CancelSubscriptionRequest(TypedDict, total=False):
    cancel_at_period_end: bool
    reason: str | None


class PortalSession(Model):
    id: str
    url: str


# Balances and banks


class Balance(Model):
    currency: str
    available_balance: str
    pending_balance: str
    held_for_disputes: str | None


class Balances(Model):
    account_id: str
    balances: list[Balance]
    total_balance_usd: str
    pending_settlements_by_day: list[dict[str, Any]] | None


class Bank(Model):
    name: str
    code: str


class BankListParams(TypedDict, total=False):
    country: str


class BankList(Model):
    country: str
    banks: list[Bank]


class ResolveBankAccountRequest(TypedDict):
    account_number: str
    bank_code: str
    country: NotRequired[str | None]


class ResolvedBankAccount(Model):
    resolved: bool
    account_name: str | None
    account_number: str | None
    message: str | None


# Payouts


class CreatePayoutDestinationRequest(TypedDict):
    currency: str
    name: NotRequired[str | None]
    label: NotRequired[str | None]
    type: NotRequired[str | None]
    destination_type: NotRequired[str | None]
    account_number: NotRequired[str | None]
    bank_code: NotRequired[str | None]
    account_name: NotRequired[str | None]
    bank_name: NotRequired[str | None]
    phone_number: NotRequired[str | None]
    mobile_provider: NotRequired[str | None]
    wallet_address: NotRequired[str | None]
    network: NotRequired[str | None]
    metadata: NotRequired[dict[str, JsonValue] | None]


class PayoutDestination(Model):
    id: str
    name: str
    type: str
    currency: str
    status: str
    is_usable: bool | None
    is_default: bool | None
    status_reason: str | None
    account_number: str | None
    account_name: str | None
    bank_code: str | None
    bank_name: str | None
    phone_number: str | None
    mobile_provider: str | None
    wallet_address: str | None
    network: str | None
    reviewed_at: str | None
    created_at: str | None
    updated_at: str | None


class PayoutDestinationListParams(TypedDict, total=False):
    currency: str
    status: Literal["pending_review", "approved", "rejected"]
    limit: int
    offset: int


class PayoutDestinationList(Model):
    destinations: list[PayoutDestination]
    total: int
    limit: int
    offset: int


class CreatePayoutQuoteRequest(TypedDict):
    from_currency: str
    to_currency: str
    amount: str
    payout_method: NotRequired[str | None]


class PayoutQuote(Model):
    quote_id: str
    from_currency: str
    to_currency: str
    from_amount: str
    to_amount: str
    exchange_rate: str
    expires_at: str


class _CreatePayoutCommon(TypedDict):
    destination: str
    reference: NotRequired[str | None]
    metadata: NotRequired[dict[str, JsonValue] | None]


class AmountPayoutRequest(_CreatePayoutCommon):
    """Same-currency payout; ``amount`` is in the destination currency."""

    amount: str


class QuotedPayoutRequest(_CreatePayoutCommon):
    """Cross-currency payout using a quote from ``payout_quotes.create``."""

    quote_id: str


# Supply exactly one of amount or quote_id.
CreatePayoutRequest = Union[AmountPayoutRequest, QuotedPayoutRequest]


class Payout(Model):
    id: str
    status: str
    amount: str
    currency: str
    source_currency: str | None
    fee: str | None
    total_debited: str | None
    destination: str | None
    reference: str | None
    failure_reason: str | None
    created_at: str | None
    completed_at: str | None


class PayoutListParams(TypedDict, total=False):
    limit: int
    offset: int
    status_filter: Literal["requested", "pending", "processing", "approved", "rejected", "completed", "failed"]


class PayoutList(Model):
    total: int
    items: list[Payout]


# Webhooks


class WebhookEvent(Model):
    id: str
    type: str
    created_at: str
    organization_id: str
    data: dict[str, Any]
