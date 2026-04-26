"""Synthetic data generator for performance stress testing.

This module generates large-scale CSV files that mimic the production schema
to benchmark engine throughput and memory limits.
"""

import csv
import random
from datetime import datetime, timedelta

from mimesis import Generic
from mimesis.locales import Locale


def generate_synthetic_data(file_path: str, row_count: int = 1_000_000) -> None:
    """Generates a synthetic CSV file mirroring the data.csv schema.

    Args:
        file_path: Path where the CSV will be saved.
        row_count: Number of rows to generate.
    """
    g = Generic(locale=Locale.EN)

    headers = [
        "InvoiceNo", "StockCode", "Description", "Quantity",
        "InvoiceDate", "UnitPrice", "CustomerID", "Country"
    ]

    countries = ["United Kingdom", "France", "Germany", "USA", "Spain", "EIRE"]
    start_date = datetime(2010, 1, 1)

    with open(file_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for i in range(row_count):
            is_cancellation = random.random() < 0.15
            invoice_no = f"{'C' if is_cancellation else ''}{536365 + i}"
            quantity = random.randint(1, 100) * (-1 if is_cancellation else 1)

            # Match production format: 12/1/2010 8:26
            invoice_date = (start_date + timedelta(minutes=i)).strftime(
                "%m/%d/%Y %H:%M"
            )

            writer.writerow([
                invoice_no,
                g.code.ean(),
                g.text.words(quantity=3),
                quantity,
                invoice_date,
                round(random.uniform(0.5, 50.0), 2),
                random.randint(12345, 18999),
                random.choice(countries)
            ])

if __name__ == "__main__":
    import sys
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
    print(f"Generating {count:,} synthetic rows...")
    generate_synthetic_data("data/stress_test.csv", count)
    print("Generation complete: data/stress_test.csv")
