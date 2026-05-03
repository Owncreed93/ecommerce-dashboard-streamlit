"""SegmentationThresholds Value Object.

This module provides the SegmentationThresholds class to handle
dynamic monetary bounds for order segmentation.
"""

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class SegmentationThresholds:
    """A Value Object representing monetary bounds for segmentation.

    This object ensures that the thresholds are immutable, non-negative,
    and logically consistent (low < high).

    Attributes:
        low_bound: The upper limit for the 'Low' category.
        high_bound: The upper limit for the 'Mid' category.
    """

    low_bound: Decimal
    high_bound: Decimal

    def __post_init__(self) -> None:
        """Validates the thresholds consistency.

        Raises:
            ValueError: If bounds are negative or inconsistent.
        """
        if self.low_bound < 0 or self.high_bound < 0:
            raise ValueError("Bounds must be non-negative.")

        if self.high_bound <= self.low_bound:
            raise ValueError("high_bound must be greater than low_bound.")
