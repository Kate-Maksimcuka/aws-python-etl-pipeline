"""Run the full local ETL pipeline."""

from extract_exchange_rates import extract_exchange_rates, save_raw_data
from transform_exchange_rates import create_summary, save_outputs, transform_rates
from create_charts import main as create_charts


def main() -> None:
    raw_data = extract_exchange_rates(days=90)
    save_raw_data(raw_data)

    clean_df = transform_rates(raw_data)
    summary_df = create_summary(clean_df)
    save_outputs(clean_df, summary_df)

    create_charts()
    print("Pipeline complete.")


if __name__ == "__main__":
    main()
