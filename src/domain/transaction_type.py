"""Enum for transaction type categorization.

This module defines the TransactionType enum to distinguish between
sales, returns, and total net transactions.
"""

from enum import Enum


class TransactionType(Enum):
    """Categorization for business transactions."""

    ALL = "All Transactions"
    SALES = "Sales Only"
    RETURNS = "Returns Only"
