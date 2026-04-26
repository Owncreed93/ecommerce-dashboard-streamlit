"""Unit tests for domain identifier Value Objects.

This module verifies that InvoiceIdentifier and CustomerIdentifier
correctly handle validation and business logic.
"""

import pytest

from domain.customer_identifier import CustomerIdentifier
from domain.invoice_identifier import InvoiceIdentifier


def test_invoice_identifier_creation() -> None:
    """Verify that a valid invoice identifier can be created."""
    invoice = InvoiceIdentifier(value="536365")
    assert invoice.value == "536365"
    assert not invoice.is_cancellation


def test_invoice_identifier_cancellation() -> None:
    """Verify that 'C' prefix identifies a cancellation."""
    invoice = InvoiceIdentifier(value="C537143")
    assert invoice.value == "C537143"
    assert invoice.is_cancellation


def test_invoice_identifier_invalid_format_raises_error() -> None:
    """Verify that non-alphanumeric characters raise a ValueError."""
    with pytest.raises(ValueError, match="Invalid characters in invoice"):
        InvoiceIdentifier(value="INV#123")


def test_customer_identifier_creation() -> None:
    """Verify that a valid customer identifier can be created."""
    customer = CustomerIdentifier(value="17850")
    assert customer.value == "17850"
    assert not customer.is_missing


def test_customer_identifier_missing_value() -> None:
    """Verify that empty or None values are handled as missing."""
    c1 = CustomerIdentifier(value="")
    c2 = CustomerIdentifier(value=None)

    assert c1.is_missing
    assert c2.is_missing


def test_identifiers_are_immutable() -> None:
    """Verify that identifiers are frozen dataclasses."""
    invoice = InvoiceIdentifier(value="123")
    customer = CustomerIdentifier(value="456")

    with pytest.raises(AttributeError):
        invoice.value = "change"  # type: ignore

    with pytest.raises(AttributeError):
        customer.value = "change"  # type: ignore
