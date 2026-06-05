"""Transform raw exchange-rate JSON into clean analytics tables."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

RAW_INPUT_PATH = Path("data/raw/exchange_rates_raw.json")
CLEAN_OUTPUT_PATH = Path("data/processed/exchange_rates_clean.csv")
SUMMARY_OUTPUT_PATH = Path("data/processed/exchange_rates_summary.csv")


def load_raw_data(input_path: Path = RAW_INPUT_PATH) -> dict:
    """Load raw exchange-rate JSON from disk."""
    return json.loads(input_path.read_text())


def transform_rates(raw_data: dict) -> pd.DataFrame:
    """Convert nested API data into a clean table."""
    rows = []
    base_currency = raw_data["base"]

    for rate_date, currencies in raw_data["rates"].items():
        for target_currency, rate in currencies.items():
            rows.append(
                {
                    "date": rate_date,
                    "base_currency": base_currency,
                    "target_currency": target_currency,
                    "exchange_rate": rate,
                }
            )

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    df["exchange_rate"] = pd.to_numeric(df["exchange_rate"])
    df = df.sort_values(["target_currency", "date"]).reset_index(drop=True)
    return df


def create_summary(clean_df: pd.DataFrame) -> pd.DataFrame:
    """Create summary metrics for each target currency."""
    summary = clean_df.groupby("target_currency").agg(
        first_date=("date", "min"),
        last_date=("date", "max"),
        average_rate=("exchange_rate", "mean"),
        minimum_rate=("exchange_rate", "min"),
        maximum_rate=("exchange_rate", "max"),
        observations=("exchange_rate", "count"),
    )
    numeric_columns = ["average_rate", "minimum_rate", "maximum_rate"]
    summary[numeric_columns] = summary[numeric_columns].round(4)
    summary = summary.reset_index()
    return summary


def save_outputs(clean_df: pd.DataFrame, summary_df: pd.DataFrame) -> None:
    """Save transformed datasets."""
    CLEAN_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    clean_df.to_csv(CLEAN_OUTPUT_PATH, index=False)
    summary_df.to_csv(SUMMARY_OUTPUT_PATH, index=False)


if __name__ == "__main__":
    raw = load_raw_data()
    clean = transform_rates(raw)
    summary = create_summary(clean)
    save_outputs(clean, summary)
    print(f"Saved clean data to {CLEAN_OUTPUT_PATH}")
    print(f"Saved summary data to {SUMMARY_OUTPUT_PATH}")
