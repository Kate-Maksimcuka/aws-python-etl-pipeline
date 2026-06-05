"""Optional script to upload processed outputs to AWS S3.

This script is not required for the local version of the project.
Use it only after configuring AWS credentials on your machine.
"""

from __future__ import annotations

import os
from pathlib import Path

import boto3
from dotenv import load_dotenv

load_dotenv()

BUCKET_NAME = os.getenv("AWS_S3_BUCKET")
FILES_TO_UPLOAD = [
    Path("data/processed/exchange_rates_clean.csv"),
    Path("data/processed/exchange_rates_summary.csv"),
]


def upload_files_to_s3() -> None:
    """Upload processed project files to an S3 bucket."""
    if not BUCKET_NAME:
        raise ValueError("Set AWS_S3_BUCKET in a .env file before running this script.")

    s3_client = boto3.client("s3")
    for file_path in FILES_TO_UPLOAD:
        key = f"exchange-rates/{file_path.name}"
        s3_client.upload_file(str(file_path), BUCKET_NAME, key)
        print(f"Uploaded {file_path} to s3://{BUCKET_NAME}/{key}")


if __name__ == "__main__":
    upload_files_to_s3()
