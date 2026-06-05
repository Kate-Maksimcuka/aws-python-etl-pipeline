# AWS Python ETL Pipeline

A beginner-friendly data engineering project that extracts exchange-rate data from a public API, transforms it with Python, saves clean datasets, and creates simple charts.

The project is designed to show the basic shape of an ETL pipeline:

**Extract → Transform → Load → Analyse**

## Project Summary

This pipeline collects recent exchange rates using GBP as the base currency and compares it against USD, EUR, JPY, CAD and AUD.

The local version saves:

- raw API data as JSON
- cleaned exchange-rate data as CSV
- summary metrics by currency
- visual charts for analysis

There is also an optional AWS script for uploading processed files to S3 once AWS credentials are configured.

## Key Skills Demonstrated

- Built a basic ETL workflow using Python
- Extracted data from a public API
- Transformed nested JSON into clean CSV tables
- Created summary metrics with pandas
- Designed charts while handling scale differences between currencies
- Uploaded processed data to Amazon S3
- Queried clean data with Amazon Athena
- Documented the workflow clearly in GitHub

## Tools Used

- Python
- pandas
- requests
- matplotlib
- AWS S3 optional extension
- Athena example SQL optional extension

## Project Structure

```text
.
├── data/
│   ├── raw/                  # Raw API response
│   └── processed/            # Clean CSV outputs
├── docs/                     # Architecture and Athena SQL example
├── outputs/
│   └── charts/               # Generated charts
├── src/                      # ETL pipeline scripts
├── .env.example              # Optional AWS config example
├── requirements.txt
└── README.md
```

## Pipeline Steps

### 1. Extract

`src/extract_exchange_rates.py` pulls exchange-rate data from the Frankfurter public API.

Output:

- `data/raw/exchange_rates_raw.json`

### 2. Transform

`src/transform_exchange_rates.py` converts the nested JSON response into clean tabular data.

Outputs:

- `data/processed/exchange_rates_clean.csv`
- `data/processed/exchange_rates_summary.csv`

### 3. Analyse

`src/create_charts.py` creates charts from the processed data.

Outputs:

- `outputs/charts/exchange_rates_dual_axis_with_jpy.png`
- `outputs/charts/indexed_exchange_rate_change.png`
- `outputs/charts/exchange_rate_percentage_range_by_currency.png`

### 4. Optional AWS Load

`src/upload_to_s3.py` can upload the processed CSV files to an S3 bucket after AWS credentials are configured locally.

## Charts

### GBP Exchange Rates With JPY on a Separate Axis

This chart shows all selected currencies in one view, but uses two y-axes because JPY is on a much larger numerical scale than the other currencies.

The left-hand y-axis is used for USD, EUR, CAD and AUD. These exchange rates are all close enough in value to be compared on the same scale. The right-hand y-axis is used for JPY, because GBP to JPY is around 210–216 during this period, while the other currencies are mostly around 1–2.

Using one shared y-axis would make the USD, EUR, CAD and AUD lines appear almost flat and difficult to read. Using a separate axis for JPY keeps the chart readable while still allowing all currencies to be shown together.

The chart should be read as a trend comparison rather than a direct comparison of raw values across the two axes. For fairer comparison of relative movement, the indexed chart below is more useful.

![GBP exchange rates with JPY on a separate axis](outputs/charts/exchange_rates_dual_axis_with_jpy.png)

### Indexed Exchange Rate Change

The selected currencies have very different exchange-rate values, so plotting them on one raw scale can make smaller-valued currencies difficult to see. To compare their movement more fairly, this chart converts each currency into an index.

Each currency starts at 100 on the first date in the dataset. Later values show how much that currency has moved relative to its own starting point.

For example:

- 100 means no change from the first date
- 102 means the exchange rate is about 2% higher than on the first date
- 98 means the exchange rate is about 2% lower than on the first date

This makes it easier to compare trends across currencies, even when one currency, such as JPY, has much larger raw exchange-rate numbers than currencies like USD or EUR.

![Indexed exchange rate change](outputs/charts/indexed_exchange_rate_change.png)

### Exchange Rate Percentage Range by Currency

The currencies in this dataset have very different exchange-rate scales. For example, GBP to JPY is around 210–216, while GBP to USD is around 1.32–1.36. If I compare the raw difference between minimum and maximum values, JPY appears much larger mainly because it is measured on a larger numerical scale.

To make the comparison fairer, this chart uses the percentage range:

```text
(maximum exchange rate - minimum exchange rate) / minimum exchange rate × 100
```

This shows relative movement within each currency over the period, rather than simply showing which currency has the largest raw numbers.

![Exchange rate percentage range by currency](outputs/charts/exchange_rate_percentage_range_by_currency.png)

## How to Run Locally

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install requirements:

```bash
pip install -r requirements.txt
```

Run the full pipeline:

```bash
python src/run_pipeline.py
```

If Matplotlib has cache permission issues, run:

```bash
MPLCONFIGDIR=.cache/matplotlib XDG_CACHE_HOME=.cache python src/run_pipeline.py
```

## Optional AWS S3 Upload

Create a `.env` file from `.env.example`:

```bash
cp .env.example .env
```

Add your bucket name:

```text
AWS_S3_BUCKET=your-bucket-name-here
```

Then run:

```bash
python src/upload_to_s3.py
```

## AWS Extension Evidence

To extend the local ETL pipeline into a basic cloud workflow, I uploaded the processed CSV outputs to Amazon S3 and queried the clean exchange-rate data using Amazon Athena.

The processed files were uploaded to an S3 bucket under an `exchange-rates/` folder. For Athena, the clean dataset was also placed in a separate `exchange-rates-clean/` folder so the table reads only the row-level exchange-rate data and not the summary file.

### S3 Processed Files

![S3 processed files](outputs/screenshots/s3_uploaded_files.png)

### Athena Query Result

![Athena query result](outputs/screenshots/athena_query_results.png)

This confirms that the cleaned CSV output can be stored in S3 and queried with SQL in Athena.

## Example Athena Query

An example Athena query is included in:

`docs/athena_example.sql`

This shows how the processed data could be queried after being uploaded to S3 and registered as an Athena table.

## What I Practised

- Building a simple ETL pipeline
- Working with a public API
- Cleaning nested JSON data into tabular CSV files
- Creating summary metrics with pandas
- Producing simple visualisations
- Structuring a GitHub project clearly
- Preparing an optional AWS S3 extension

## Next Improvements

- Add automated data validation checks
- Add a scheduled pipeline run
- Create an Athena table definition
- Add a small dashboard using Streamlit or Power BI
