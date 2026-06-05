"""Extract daily exchange rates from the Frankfurter public API."""

from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

import requests

API_URL = "https://api.frankfurter.app"
BASE_CURRENCY = "GBP"
TARGET_CURRENCIES = ["USD", "EUR", "JPY", "CAD", "AUD"]
RAW_OUTPUT_PATH = Path("data/raw/exchange_rates_raw.json")


def get_date_range(days: int = 90) -> tuple[str, str]:
    """Return start and end dates for the API request."""
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    return start_date.isoformat(), end_date.isoformat()


def extract_exchange_rates(days: int = 90) -> dict:
    """Fetch exchange rates for the selected currencies."""
    start_date, end_date = get_date_range(days)
    symbols = ",".join(TARGET_CURRENCIES)
    url = f"{API_URL}/{start_date}..{end_date}"
    params = {"from": BASE_CURRENCY, "to": symbols}

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def save_raw_data(data: dict, output_path: Path = RAW_OUTPUT_PATH) -> None:
    """Save raw API response as JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, indent=2))


if __name__ == "__main__":
    raw_data = extract_exchange_rates(days=90)
    save_raw_data(raw_data)
    print(f"Saved raw data to {RAW_OUTPUT_PATH}")
