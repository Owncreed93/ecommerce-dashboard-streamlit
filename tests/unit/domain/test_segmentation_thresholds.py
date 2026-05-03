"""Unit tests for the SegmentationThresholds Value Object.

This module ensures that the segmentation thresholds are immutable,
properly validated, and logically consistent.
"""

from dataclasses import FrozenInstanceError
from decimal import Decimal

import pytest

from domain.segmentation_thresholds import SegmentationThresholds


def test_segmentation_thresholds_creation() -> None:
    """Verify that thresholds are correctly initialized."""
    low = Decimal("50.0")
    high = Decimal("200.0")
    thresholds = SegmentationThresholds(low_bound=low, high_bound=high)

    assert thresholds.low_bound == low
    assert thresholds.high_bound == high


def test_segmentation_thresholds_immutability() -> None:
    """Verify that the object is frozen and cannot be modified."""
    thresholds = SegmentationThresholds(
        low_bound=Decimal("50"), high_bound=Decimal("200")
    )

    with pytest.raises(FrozenInstanceError):
        thresholds.low_bound = Decimal("60")  # type: ignore


def test_segmentation_thresholds_validation_negative() -> None:
    """Verify that negative bounds raise a ValueError."""
    with pytest.raises(ValueError, match="Bounds must be non-negative"):
        SegmentationThresholds(low_bound=Decimal("-1"), high_bound=Decimal("100"))


def test_segmentation_thresholds_validation_logic() -> None:
    """Verify that high_bound must be greater than low_bound."""
    with pytest.raises(ValueError, match="high_bound must be greater than low_bound"):
        SegmentationThresholds(low_bound=Decimal("100"), high_bound=Decimal("50"))


def test_segmentation_thresholds_slots() -> None:
    """Verify that slots are used for memory efficiency."""
    thresholds = SegmentationThresholds(
        low_bound=Decimal("50"), high_bound=Decimal("200")
    )
    assert not hasattr(thresholds, "__dict__")
