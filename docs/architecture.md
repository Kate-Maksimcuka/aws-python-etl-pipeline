# Project Architecture

```mermaid
flowchart LR
    A[Frankfurter API] --> B[Python extract script]
    B --> C[Raw JSON file]
    C --> D[Python transform script]
    D --> E[Clean CSV]
    D --> F[Summary CSV]
    E --> G[Charts]
    F --> G
    E -. optional .-> H[AWS S3]
    F -. optional .-> H[AWS S3]
    H -. optional .-> I[AWS Athena]
```

## Local Pipeline

The local version extracts exchange-rate data from a public API, saves a raw JSON file, transforms it into clean CSV outputs, and creates charts.

## Optional AWS Extension

After AWS credentials are configured, the processed CSV files can be uploaded to S3. They can then be queried with Athena as a simple cloud data workflow.
