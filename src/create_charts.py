"""Create simple portfolio charts from processed exchange-rate data."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

CLEAN_INPUT_PATH = Path("data/processed/exchange_rates_clean.csv")
SUMMARY_INPUT_PATH = Path("data/processed/exchange_rates_summary.csv")
CHART_DIR = Path("outputs/charts")


def save_line_chart(clean_df: pd.DataFrame) -> None:
    """Save a line chart showing exchange-rate movement over time."""
    plt.figure(figsize=(11, 6))
    for currency in sorted(clean_df["target_currency"].unique()):
        currency_df = clean_df[clean_df["target_currency"] == currency]
        plt.plot(currency_df["date"], currency_df["exchange_rate"], label=currency)

    plt.title("GBP Exchange Rates Over Time")
    plt.xlabel("Date")
    plt.ylabel("Exchange rate from GBP")
    plt.legend(title="Currency")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "exchange_rates_over_time.png", dpi=160)
    plt.close()


def save_average_rate_chart(summary_df: pd.DataFrame) -> None:
    """Save a bar chart of average exchange rates."""
    plot_df = summary_df.sort_values("average_rate", ascending=False)
    plt.figure(figsize=(9, 5))
    plt.bar(plot_df["target_currency"], plot_df["average_rate"])
    plt.title("Average Exchange Rate by Currency")
    plt.xlabel("Target currency")
    plt.ylabel("Average exchange rate from GBP")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "average_exchange_rate_by_currency.png", dpi=160)
    plt.close()


def save_volatility_chart(clean_df: pd.DataFrame) -> None:
    """Save a chart showing rate range by currency."""
    range_df = (
        clean_df.groupby("target_currency")["exchange_rate"]
        .agg(rate_range=lambda values: values.max() - values.min())
        .reset_index()
        .sort_values("rate_range", ascending=False)
    )

    plt.figure(figsize=(9, 5))
    plt.bar(range_df["target_currency"], range_df["rate_range"])
    plt.title("Exchange Rate Range by Currency")
    plt.xlabel("Target currency")
    plt.ylabel("Maximum minus minimum rate")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "exchange_rate_range_by_currency.png", dpi=160)
    plt.close()


def main() -> None:
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    clean_df = pd.read_csv(CLEAN_INPUT_PATH, parse_dates=["date"])
    summary_df = pd.read_csv(SUMMARY_INPUT_PATH)

    save_line_chart(clean_df)
    save_average_rate_chart(summary_df)
    save_volatility_chart(clean_df)
    print(f"Saved charts to {CHART_DIR}")


if __name__ == "__main__":
    main()
