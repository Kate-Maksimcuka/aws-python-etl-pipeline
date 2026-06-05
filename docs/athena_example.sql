-- Example Athena query for the processed exchange-rate data after upload to S3.
-- This is illustrative; table creation depends on your S3 bucket and Athena database setup.

SELECT
    target_currency,
    ROUND(AVG(exchange_rate), 4) AS average_exchange_rate,
    MIN(exchange_rate) AS minimum_exchange_rate,
    MAX(exchange_rate) AS maximum_exchange_rate,
    COUNT(*) AS observations
FROM exchange_rates_clean
GROUP BY target_currency
ORDER BY average_exchange_rate DESC;
