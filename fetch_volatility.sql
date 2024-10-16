WITH daily_prices AS (
    SELECT 
        date_trunc('day', minute) AS time,
        AVG(price) AS price
    FROM 
        prices.usd
    WHERE 
        symbol = 'ETH'
        AND contract_address IS NULL
    GROUP BY 
        1
),
price_changes AS (
    SELECT 
        time,
        price,
        LAG(price) OVER (ORDER BY time) AS previous_price,
        (price - LAG(price) OVER (ORDER BY time)) AS price_change
    FROM 
        daily_prices
),
volatility AS (
    SELECT 
        time,
        price_change,
        STDDEV(price_change) OVER () AS stddev_change,
        AVG(price_change) OVER () AS avg_change
    FROM 
        price_changes
)
SELECT 
    time,
    price_change,
    stddev_change,
    avg_change,
    CASE 
        WHEN price_change > 0 THEN price_change  -- New column for positive price changes
        ELSE NULL 
    END AS positive_price_change,  -- Column for positive price changes
    CASE 
        WHEN price_change < 0 THEN price_change  -- Existing column for negative price changes
        ELSE NULL 
    END AS negative_price_change  -- Column for negative price changes
FROM 
    volatility
WHERE 
    ABS(price_change) > (avg_change + 2 * stddev_change)  -- Example threshold for high volatility
    AND time BETWEEN TIMESTAMP '2023-01-01 00:00:00' AND TIMESTAMP '2024-01-31 23:59:59'  -- Use TIMESTAMP for date range
ORDER BY 
    time;