"""Unit tests for the Money Value Object.

This module contains tests to verify immutability, precision,
and business logic for financial calculations.
"""

from decimal import Decimal

import pytest

from domain.money import Money


def test_money_creation_with_valid_amount() -> None:
    """Verify that Money can be created with a valid Decimal amount."""
    amount = Decimal("100.50")
    money = Money(amount=amount, currency="USD")
    assert money.amount == amount
    assert money.currency == "USD"


def test_money_is_immutable() -> None:
    """Verify that Money object is immutable (frozen dataclass)."""
    money = Money(amount=Decimal("10.00"), currency="USD")
    with pytest.raises(AttributeError):
        money.amount = Decimal("20.00")  # type: ignore


def test_money_from_float_converts_to_decimal() -> None:
    """Verify that Money handles float input by converting to Decimal."""
    money = Money.from_float(100.5, "USD")
    assert isinstance(money.amount, Decimal)
    assert money.amount == Decimal("100.5")


def test_money_addition_same_currency() -> None:
    """Verify addition of two Money objects with the same currency."""
    m1 = Money(Decimal("10.00"), "USD")
    m2 = Money(Decimal("5.50"), "USD")
    result = m1 + m2
    assert result.amount == Decimal("15.50")
    assert result.currency == "USD"


def test_money_addition_different_currency_fails() -> None:
    """Verify that adding different currencies raises a ValueError."""
    m1 = Money(Decimal("10.00"), "USD")
    m2 = Money(Decimal("5.50"), "EUR")
    with pytest.raises(ValueError, match="Cannot add different currencies"):
        _ = m1 + m2


def test_money_invalid_currency_raises_error() -> None:
    """Verify that an empty currency raises a ValueError."""
    with pytest.raises(ValueError, match="Currency cannot be empty"):
        Money(Decimal("10.00"), "")
