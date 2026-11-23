-- Warehouse validation
-- Expected: 530104 rows and 10666684.54 GBP in both tables.
-- Positive sales amounts are not net revenue.

SELECT
    'staging' AS table_name,
    COUNT(*) AS row_count,
    ROUND(SUM(quantity * unit_price), 2) AS positive_sales_amount
FROM dw.stg_sales
UNION ALL
SELECT
    'fact_sales',
    COUNT(*),
    ROUND(SUM(line_amount), 2)
FROM dw.fact_sales;

-- Expected sales rows: Known = 397884; Unknown = 132220.
-- Unknown is a missing-identity category, not one real customer.

SELECT
    c.customer_status,
    COUNT(*) AS sales_rows,
    ROUND(SUM(f.line_amount), 2) AS positive_sales_amount
FROM dw.fact_sales AS f
JOIN dw.dim_customer AS c
    ON c.customer_key = f.customer_key
GROUP BY c.customer_status
ORDER BY c.customer_status;

SELECT
    COUNT(*) FILTER (
        WHERE p.product_key IS NULL
    ) AS urunsuz_satis,
    COUNT(*) FILTER (
        WHERE c.customer_key IS NULL
    ) AS musterisiz_satis,
    COUNT(*) FILTER (
        WHERE d.date_key IS NULL
    ) AS tarihsiz_satis
FROM dw.fact_sales f
LEFT JOIN dw.dim_product p
    ON f.product_key = p.product_key
LEFT JOIN dw.dim_customer c
    ON f.customer_key = c.customer_key
LEFT JOIN dw.dim_date d
    ON f.date_key = d.date_key;