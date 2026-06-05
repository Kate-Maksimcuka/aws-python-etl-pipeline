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
    """Save line charts showing exchange-rate movement over time."""
    major_currency_df = clean_df[clean_df["target_currency"] != "JPY"]
    plt.figure(figsize=(11, 6))
    for currency in sorted(major_currency_df["target_currency"].unique()):
        currency_df = major_currency_df[major_currency_df["target_currency"] == currency]
        plt.plot(currency_df["date"], currency_df["exchange_rate"], label=currency)

    plt.title("GBP Exchange Rates Over Time Excluding JPY")
    plt.xlabel("Date")
    plt.ylabel("Exchange rate from GBP")
    plt.legend(title="Currency")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "exchange_rates_over_time_excluding_jpy.png", dpi=160)
    plt.close()

    jpy_df = clean_df[clean_df["target_currency"] == "JPY"]
    plt.figure(figsize=(11, 6))
    plt.plot(jpy_df["date"], jpy_df["exchange_rate"], color="#8c564b", label="JPY")
    plt.title("GBP to JPY Exchange Rate Over Time")
    plt.xlabel("Date")
    plt.ylabel("Exchange rate from GBP")
    plt.legend(title="Currency")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "gbp_to_jpy_exchange_rate.png", dpi=160)
    plt.close()


def save_dual_axis_chart(clean_df: pd.DataFrame) -> None:
    """Save one chart with JPY on a separate axis because it has a different scale."""
    major_currency_df = clean_df[clean_df["target_currency"] != "JPY"]
    jpy_df = clean_df[clean_df["target_currency"] == "JPY"]

    fig, left_axis = plt.subplots(figsize=(11, 6))
    for currency in sorted(major_currency_df["target_currency"].unique()):
        currency_df = major_currency_df[major_currency_df["target_currency"] == currency]
        left_axis.plot(currency_df["date"], currency_df["exchange_rate"], label=currency)

    left_axis.set_xlabel("Date")
    left_axis.set_ylabel("Exchange rate from GBP, excluding JPY")
    left_axis.grid(alpha=0.3)

    right_axis = left_axis.twinx()
    right_axis.plot(
        jpy_df["date"],
        jpy_df["exchange_rate"],
        color="#8c564b",
        linestyle="--",
        label="JPY",
    )
    right_axis.set_ylabel("GBP to JPY exchange rate")

    left_lines, left_labels = left_axis.get_legend_handles_labels()
    right_lines, right_labels = right_axis.get_legend_handles_labels()
    left_axis.legend(
        left_lines + right_lines,
        left_labels + right_labels,
        title="Currency",
        loc="upper left",
    )

    plt.title("GBP Exchange Rates Over Time With JPY on Separate Axis")
    fig.tight_layout()
    plt.savefig(CHART_DIR / "exchange_rates_dual_axis_with_jpy.png", dpi=160)
    plt.close()


def save_indexed_line_chart(clean_df: pd.DataFrame) -> None:
    """Save an indexed chart so currencies with different scales can be compared."""
    indexed_df = clean_df.copy()
    indexed_df["indexed_rate"] = indexed_df.groupby("target_currency")[
        "exchange_rate"
    ].transform(lambda values: values / values.iloc[0] * 100)

    plt.figure(figsize=(11, 6))
    for currency in sorted(indexed_df["target_currency"].unique()):
        currency_df = indexed_df[indexed_df["target_currency"] == currency]
        plt.plot(currency_df["date"], currency_df["indexed_rate"], label=currency)

    plt.title("Indexed Exchange Rate Change Over Time")
    plt.xlabel("Date")
    plt.ylabel("Index, first date = 100")
    plt.legend(title="Currency")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "indexed_exchange_rate_change.png", dpi=160)
    plt.close()


def save_percentage_range_chart(clean_df: pd.DataFrame) -> None:
    """Save a comparable percentage range chart for all currencies."""
    range_df = clean_df.groupby("target_currency")["exchange_rate"].agg(["min", "max"])
    range_df["percentage_range"] = (range_df["max"] - range_df["min"]) / range_df[
        "min"
    ] * 100
    range_df = range_df.reset_index().sort_values("percentage_range", ascending=False)

    plt.figure(figsize=(9, 5))
    plt.bar(range_df["target_currency"], range_df["percentage_range"])
    plt.title("Exchange Rate Range by Currency (%)")
    plt.xlabel("Target currency")
    plt.ylabel("Percentage range over the period")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "exchange_rate_percentage_range_by_currency.png", dpi=160)
    plt.close()


def main() -> None:
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    clean_df = pd.read_csv(CLEAN_INPUT_PATH, parse_dates=["date"])
    summary_df = pd.read_csv(SUMMARY_INPUT_PATH)

    save_line_chart(clean_df)
    save_dual_axis_chart(clean_df)
    save_indexed_line_chart(clean_df)
    save_percentage_range_chart(clean_df)
    print(f"Saved charts to {CHART_DIR}")


if __name__ == "__main__":
    main()
